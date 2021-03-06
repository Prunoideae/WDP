from wdp.task import Arg, Output, Workflow
from wdp.task import run_cmd, internal, taskinfo, task
from wdp.events import PreExecutionEvent, PostExecutionEvent, PreParsingEvent
from wdp.eventbus.bus import subscribe
from wdp.eventbus.event import CancellEvent

from wdp.task import Arg, task, run_cmd

import asyncio


@task(help='Some example')
def some(
    arg1: int = Arg(
        name='input',
        var_type=int
    )
):
    print(arg1)
    return 1


@task(help='Other example')
def fun(
    arg1: str = Arg(
        name='some0'
    )
):
    print(arg1)
    return Output('bar', arg1)


if __name__ == "__main__":
    run_cmd(program='Hello', help='First task!', show_task=True)
