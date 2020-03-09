from wdp.task import Arg, task, run_cmd, run_internal, taskinfo
from wdp.events import PreExecutionEvent, PostExecutionEvent, PreParsingEvent
from wdp.eventbus.bus import subscribe
from wdp.eventbus.event import CancellEvent


@task(help='a test command')
def test(
        arg1: str = Arg(
            name='test',
            short='t',
            help='test parameter',
            required=True
        )
):
    print(arg1)
    return 'returned from test'


@taskinfo(foo='bar')
@task(help='internal call command')
def call(
        arg1: str = Arg(
            name='fun',
            short='f',
            help='some arg',
            required=True
        ),
        const1=1
):
    print(call.foo)


@subscribe
def execute(event: PreParsingEvent):
    print(f"Execution of {event.task.command} started.")
    print(f"Received arguments : {event.args}")

    if 'test' in event.args and event.args['test'] == 'bar':
        event.args['test'] = 'foo'


@subscribe
def some(event: [PostExecutionEvent, PreExecutionEvent]):
    print(
        f"Execution of {event.task.command}. Type : {event.__class__.__name__}")


if __name__ == '__main__':
    run_cmd('test', 'a test program')
