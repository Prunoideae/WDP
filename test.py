from magic.magic import Arg, task, run_cmd, run_internal
from magic.events import ProgramStartedEvent
from magic.eventbus.bus import subscribe


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
    return 'kwa'


@task(help='internal call command')
def call():
    print(run_internal(test, test='bar'))


@subscribe
def started(event: ProgramStartedEvent):
    print('I am started!')


if __name__ == '__main__':
    run_cmd('test', 'a test program')
