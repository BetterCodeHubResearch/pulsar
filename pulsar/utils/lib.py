import os

if os.environ.get('PULSARPY', 'no') == 'yes':
    HAS_C_EXTENSIONS = False
else:
    HAS_C_EXTENSIONS = True
    try:
        from .clib import (
            EventHandler, ProtocolConsumer, Protocol, Producer, WsgiProtocol,
            AbortEvent, RedisParser, WsgiResponse, wsgi_cached, http_date,
            FrameParser
        )
    except ImportError:
        HAS_C_EXTENSIONS = False


if not HAS_C_EXTENSIONS:
    from .pylib.protocols import  ProtocolConsumer, Protocol, Producer  # noqa
    from .pylib.events import EventHandler, AbortEvent          # noqa
    from .pylib.wsgi import WsgiProtocol, http_date             # noqa
    from .pylib.wsgiresponse import WsgiResponse, wsgi_cached   # noqa
    from .pylib.redisparser import RedisParser                  # noqa
    from .pylib.websocket import FrameParser                    # noqa


__all__ = [
    'HAS_C_EXTENSIONS',
    'AbortEvent',
    'EventHandler',
    'ProtocolConsumer',
    'Protocol',
    'WsgiProtocol',
    'WsgiResponse',
    'wsgi_cached',
    'http_date',
    'RedisParser'
]