import datetime
import functools


def fix_message_timestamp(func):
    @functools.wraps(func)
    def inner(message):
        # Fix `pamqp` naive timestamp
        if message.timestamp:
            message.timestamp = message.timestamp.replace(tzinfo=datetime.timezone.utc)

        return func(message)

    return inner
