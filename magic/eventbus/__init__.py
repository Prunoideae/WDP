"""Event subscriber and poster of Magic"""

from .bus import (
    post,
    subscribe,
)

from .event import (
    EventBase,
    EventCommon,
    EventExplicit,
    NotCancellableError,
    Cancelled
)
