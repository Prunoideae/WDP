from wdp.task import Arg, task, run_cmd, run_internal
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
    print('internal calling test')
    print(const1)
    print(f'call result is {run_internal(test, test=arg1, rua="rua")}')


@subscribe
def execute(event: PreParsingEvent):
    print(f"Execution of {event.task.command} started.")
    print(f"Received arguments : {event.args}")
    if 'test' in event.args and event.args['test'] == 'bar':
        event.cancel()


@subscribe
def cancel(event: CancellEvent(PreParsingEvent)):
    print(event)
    print(f"Execution of {event.event.task.command} was cancelled.")


@subscribe
def done(event: [PostExecutionEvent, PreExecutionEvent]):
    print(f"Execution of {event.task.command}. {event}")


if __name__ == '__main__':
    run_cmd('test', 'a test program')
