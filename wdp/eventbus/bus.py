from functools import partial, wraps
from .event import EventBase, EventCommon, CancellEvent, Cancelled
from inspect import signature as _signature
from typing import Iterable

__eventbus__ = {}


def post(event: EventBase):
    triggered = [event.__class__]

    # CancelEvent will NOT trigger event chain
    if not isinstance(event, CancellEvent):
        def recursive(clazz, trigger: list):
            for base in clazz.__bases__:
                if issubclass(base, EventBase) and \
                    base not in trigger and \
                        base != object:
                    trigger.append(base)
                    recursive(base, trigger)

        recursive(event.__class__, triggered)

        triggered = [x for x in triggered if x in __eventbus__]

        try:
            for t in triggered:
                if t in __eventbus__:
                    for hook in __eventbus__[t]:
                        hook[0](event)
        except Cancelled:
            if isinstance(event, EventCommon):
                cancelled = CancellEvent(event)
                post(cancelled)
    else:
        if (event.__class__, event.event.__class__) in __eventbus__:
            for hook in __eventbus__[(event.__class__, event.event.__class__)]:
                hook[0](event)


def subscribe(func=None, *, priority=0):
    if func is None:
        return partial(subscribe, priority=priority)

    anno_dict = list(func.__annotations__.items())

    sig = _signature(func)

    if len(sig.parameters) != 1 or len(anno_dict) != 1:
        raise TypeError(
            "Hook requires and only requires 1 annotated parameter!")

    event = anno_dict[0][1]

    if isinstance(event, Iterable):
        for e in event:
            if isinstance(e, CancellEvent):
                e = (CancellEvent, e.event)
            if e not in __eventbus__:
                __eventbus__[e] = []

            __eventbus__[e].append((func, priority))
            __eventbus__[e].sort(key=lambda x: x[1], reverse=True)
    else:
        if isinstance(event, CancellEvent):
            event = (CancellEvent, event.event)
        if event not in __eventbus__:
            __eventbus__[event] = []

        __eventbus__[event].append((func, priority))
        __eventbus__[event].sort(key=lambda x: x[1], reverse=True)
    return func
