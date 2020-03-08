from .eventbus.event import EventCommon as _EventCommon
from .eventbus.event import EventExplicit as _EventExplicit


class ProgramStartedEvent(_EventCommon):
    pass


class PreExecutionEvent(_EventCommon):

    def __init__(self, task, args: dict):
        super().__init__()
        self.task = task
        self.args = args


class PreParsingEvent(_EventCommon):

    def __init__(self, task, args: dict):
        super().__init__()
        self.args = args
        self.task = task


class PostParsingEvent(_EventExplicit):

    def __init__(self, args: dict):
        super().__init__()


class PostExecutionEvent(_EventExplicit):

    def __init__(self, task, ret):
        super().__init__()
        self.task = task
        self.result = ret


class ProgramFinishedEvent(_EventExplicit):
    pass
