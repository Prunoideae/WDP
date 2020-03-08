class Cancelled(Exception):
    pass


class NotCancellableError(Exception):
    pass


class EventBase():
    def __init__(self):
        self.cancelled = False

    def cancel(self):
        self.cancelled = True
        raise Cancelled()


class EventCommon(EventBase):
    def __init__(self):
        super().__init__()

    class Cancelled(EventBase):
        def __init__(self, event):
            super().__init__()
            self.event = event

        def cancel(self):
            raise NotCancellableError("This event is not cancellable!")


class EventExplicit(EventCommon):
    def __init__(self):
        super().__init__()

    def cancel(self):
        raise NotCancellableError("This event is not cancellable!")


class CancellEvent(EventExplicit):
    def __init__(self, event):
        super().__init__()
        self.event = event
