import aio_pika
import asyncio
import inspect
import logging
import pydantic
import socket
import time

from . import errors
from .models import Request, Response
from .types import Message, Priority
from .utils import fix_message_timestamp


logger = logging.getLogger(__name__)


class RpcServer:
    def __init__(self, service_name):
        self._service_name = service_name
        self._app_id = f"{service_name}@{socket.gethostname()}"

        self._handlers = {}

        self._reset()

        self.bind(self._ping)
        self.bind(self._help)

    def _reset(self):
        self._connection = None
        self._channel = None
        self._exchange = None
        self._queue = None

    def bind(self, handler):
        if not inspect.iscoroutinefunction(handler):
            raise TypeError("Handlers must be coroutine functions")

        if handler.__name__ in self._handlers:
            raise KeyError(f"Handler {handler.__name__} already defined")

        self._handlers[handler.__name__] = pydantic.validate_call(
            handler,
            validate_return=True,
        )

        return handler

    async def start(self, connection_string, prefetch_count=1):
        if self._connection:
            raise RuntimeError("Already started")

        connection = self._connection = await aio_pika.connect_robust(connection_string)
        channel = self._channel = await connection.channel()
        await channel.set_qos(prefetch_count=prefetch_count)

        exchange = self._exchange = await channel.declare_exchange(
            name=f"service.{self._service_name}",
            type=aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        queue = self._queue = await channel.declare_queue(
            name=f"service.{self._service_name}",
            durable=True,
            arguments={
                "x-max-priority": max(Priority),
            },
        )

        await queue.bind(exchange, "#")
        await queue.consume(fix_message_timestamp(self._on_message))

    async def stop(self):
        connection = self._connection
        if connection:
            self._reset()
            await connection.close()

    async def serve_forever(self, connection_string):
        await self.start(connection_string)
        try:
            await asyncio.Future()
        finally:
            await self.stop()

    async def _on_message(self, message):
        timings = [(f"queue.consumed by {self._app_id}", time.time())]

        logger.debug(
            "[MID:%s] Got `%s` message from `%s` service",
            message.message_id,
            message.type or "[untyped]",
            message.app_id or "unknown",
        )

        if message.type != "rpc.request":
            logger.warning(
                "[MID:%s] Unexpected message type: `%s`",
                message.message_id,
                message.type,
            )
            await message.reject()
            return

        if message.reply_to and not message.correlation_id:
            logger.warning("[MID:%s] `correlation_id` is not set", message.message_id)
            await message.reject()
            return

        published_timestamp = None
        if message.timestamp:
            published_timestamp = message.timestamp.timestamp()
            timings.insert(0, ("queue.published", published_timestamp))

        deadline = None
        if published_timestamp and message.expiration:
            deadline = published_timestamp + message.expiration

        try:
            timings.append(("execution.started", time.time()))
            response = await asyncio.wait_for(
                self._process_message(message),
                timeout=(deadline - time.time()) if deadline else None,
            )
            timings.append(("execution.completed", time.time()))
        except asyncio.TimeoutError:
            logger.info(
                "[MID:%s] [CID:%s] Execution of `%s` from `%s` service timed out",  # noqa: E501
                message.message_id,
                message.correlation_id,
                message.type,
                message.app_id or "unknown",
            )

            await message.ack()
            return

        response.timings += timings

        if message.reply_to:
            response_message = Message(
                body=response,
                app_id=self._app_id,
                priority=message.priority,
                correlation_id=message.correlation_id,
                expiration=(deadline - time.time()) if deadline else None,
                type="rpc.response",
            )

            await message.channel.basic_publish(
                body=response_message.body,
                routing_key=message.reply_to,
                properties=response_message.properties,
            )

        await message.ack()

        logger.info(
            "[MID:%s] [CID:%s] Handled `%s` from `%s` service, success: %s",  # noqa: E501
            message.message_id,
            message.correlation_id,
            message.type,
            message.app_id or "unknown",
            response.error is None,
        )

    @Response.wrap_errors
    async def _process_message(self, message) -> Response:
        if message.content_type != "application/msgpack":
            raise errors.ParsingError(
                f"Got a message with unknown content type: {message.content_type}"
            )

        try:
            request = Request.model_validate_msgpack(message.body)
        except ValueError as error:
            raise errors.ParsingError(f"Message deserialization failed `{error!r}`")

        response = await self._process_request(request)
        response.context = request.context
        response.timings = request.timings

        logger.debug(
            "[MID:%s] Processed `%s` to method `%s`, success: %s",
            message.message_id,
            message.type,
            request.method_name,
            response.error is None,
        )

        return response

    @Response.wrap_errors
    async def _process_request(self, request) -> Response:
        handler = self._handlers.get(request.method_name)
        if handler is None:
            raise errors.UnknownMethodError(request.method_name)

        try:
            result = await handler(**request.arguments)
        except Exception as error:
            raise errors.ExecutionError(repr(error))

        if isinstance(result, pydantic.BaseModel):
            result = result.model_dump()

        return Response(result=result)

    async def _ping(self) -> None:
        return None

    async def _help(self):
        """
        Returns methods list
        """
        return {
            "methods": [
                {
                    "method_name": method_name,
                    "signature": f"{method_name}{inspect.signature(handler)}",
                    "description": handler.__doc__,
                }
                for method_name, handler in self._handlers.items()
            ]
        }
