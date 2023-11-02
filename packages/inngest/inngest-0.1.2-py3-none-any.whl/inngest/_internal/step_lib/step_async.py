import datetime
import inspect
import typing

from inngest._internal import (
    client_lib,
    event_lib,
    execution,
    result,
    transforms,
    types,
)

from . import base


class Step(base.StepBase):
    def __init__(
        self,
        client: client_lib.Inngest,
        memos: dict[str, object],
        step_id_counter: base.StepIDCounter,
    ) -> None:
        self._client = client
        self._memos = memos
        self._step_id_counter = step_id_counter

    @typing.overload
    async def run(
        self,
        step_id: str,
        handler: typing.Callable[[], typing.Awaitable[types.SerializableT]],
    ) -> types.SerializableT:
        ...

    @typing.overload
    async def run(
        self,
        step_id: str,
        handler: typing.Callable[[], types.SerializableT],
    ) -> types.SerializableT:
        ...

    async def run(
        self,
        step_id: str,
        handler: typing.Callable[[], typing.Awaitable[types.SerializableT]]
        | typing.Callable[[], types.SerializableT],
    ) -> types.SerializableT:
        """
        Run logic that should be retried on error and memoized after success.

        Args:
            step_id: Unique step ID within the function. If the same step ID is
                encountered multiple times then it'll get an index suffix.
            handler: The logic to run. Can be async or sync.
        """

        hashed_id = self._get_hashed_id(step_id)

        memo = self._get_memo(hashed_id)
        if memo is not types.EmptySentinel:
            return memo  # type: ignore

        if inspect.iscoroutinefunction(handler):
            output = await handler()
        else:
            output = handler()

        # Check whether output is serializable
        match transforms.dump_json(output):
            case result.Ok(_):
                pass
            case result.Err(err):
                raise err

        raise base.Interrupt(
            hashed_id=hashed_id,
            data=output,
            display_name=step_id,
            op=execution.Opcode.STEP,
            name=step_id,
        )

    async def send_event(
        self,
        step_id: str,
        events: event_lib.Event | list[event_lib.Event],
    ) -> list[str]:
        """
        Send an event or list of events.
        """

        async def fn() -> list[str]:
            return await self._client.send(events)

        return await self.run(step_id, fn)

    async def sleep(
        self,
        step_id: str,
        duration: int | datetime.timedelta,
    ) -> None:
        """
        Sleep for a duration.

        Args:
            duration: The number of milliseconds to sleep.
        """

        if isinstance(duration, int):
            until = datetime.datetime.utcnow() + datetime.timedelta(
                milliseconds=duration
            )
        else:
            until = datetime.datetime.utcnow() + duration

        return await self.sleep_until(step_id, until)

    async def sleep_until(
        self,
        step_id: str,
        until: datetime.datetime,
    ) -> None:
        """
        Sleep until a specific time.
        """

        hashed_id = self._get_hashed_id(step_id)

        memo = self._get_memo(hashed_id)
        if memo is not types.EmptySentinel:
            return memo  # type: ignore

        raise base.Interrupt(
            hashed_id=hashed_id,
            display_name=step_id,
            name=transforms.to_iso_utc(until),
            op=execution.Opcode.SLEEP,
        )

    async def wait_for_event(
        self,
        step_id: str,
        *,
        event: str,
        if_exp: str | None = None,
        timeout: int | datetime.timedelta,
    ) -> event_lib.Event | None:
        """
        Wait for an event to be sent.

        Args:
            event: Event name.
            if_exp: An expression to filter events.
            timeout: The maximum number of milliseconds to wait for the event.
        """

        hashed_id = self._get_hashed_id(step_id)

        memo = self._get_memo(hashed_id)
        if memo is not types.EmptySentinel:
            if memo is None:
                # Timeout
                return None

            # Fulfilled by an event
            return event_lib.Event.model_validate(memo)

        match transforms.to_duration_str(timeout):
            case result.Ok(timeout_str):
                pass
            case result.Err(err):
                raise err

        match base.WaitForEventOpts(
            if_exp=if_exp,
            timeout=timeout_str,
        ).to_dict():
            case result.Ok(opts):
                pass
            case result.Err(err):
                raise err

        raise base.Interrupt(
            hashed_id=hashed_id,
            display_name=step_id,
            name=event,
            op=execution.Opcode.WAIT_FOR_EVENT,
            opts=opts,
        )
