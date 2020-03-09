from functools import partial as _partial
from functools import wraps as _wraps
import inspect as _inspect
import argparse as _argparse
from . import events as _events
from .eventbus import bus as _bus

__registry__ = {}


class Arg():

    def __init__(self, name, short=None, help=None, required: bool = False, default=None, choices=None, meta: str = None, validator=None, var_type=None):
        super().__init__()
        self.help = help
        self.required = required
        self.default = default
        self.choices = choices
        self.callback = validator
        self.name = name
        self.short = short

        self.var_type = str
        if var_type:
            self.var_type = var_type
        elif self.default is not None:
            self.var_type = type(self.default)

        if meta is None:
            self.meta = self.var_type.__name__.upper()
        else:
            self.meta = meta.upper()

    def validate(self, value):
        if self.callback is not None:
            return self.callback(value)
        return True

    def parser(self, parser: _argparse._ActionsContainer):
        flags = [f'--{self.name}']

        if self.short:
            flags.append(f'-{self.short}')
        options = {
            'default': self.default,
            'required': self.required,
            'help': self.help + (f'(default {self.default})' if self.default is not None else '')
        }

        if type(self.default) is bool:
            options['actions'] = 'store_false' if self.default else 'store_true',
        elif self.choices is not None:
            options['choices'] = self.choices
        else:
            options['type'] = self.var_type
            options['metavar'] = f'<{self.meta}>',
        parser.add_argument(*flags, **options)


class Task():

    def __init__(self, func, help):
        super().__init__()
        sig = _inspect.signature(func)

        self.help = help
        self.func = func
        self.arguments = {}
        self.command = func.__name__

        for k, v in sig.parameters.items():
            if isinstance(v.default, Arg):
                if v.annotation is not None and v.default.var_type is None:
                    v.default.type = v.annotation
                self.arguments[v.default.name] = (k, v.default)

    def run(self, args: dict):

        arg_conv = {}
        for k, v in self.arguments.items():
            if k not in args:
                if not v[1].required:
                    arg_conv[v[0]] = v[1].default
                else:
                    raise KeyError('Required argument not found!')
            pass

        pre = _events.PreParsingEvent(self, args)
        _bus.post(pre)
        if pre.cancelled:
            return None
        args = pre.args

        valid = True
        for a, v in args.items():
            if a in self.arguments:
                par, arg = self.arguments[a]
                valid = valid and arg.validate(v)
                if valid:
                    arg_conv[par] = v

        if valid:

            pre = _events.PreExecutionEvent(self, arg_conv)
            _bus.post(pre)
            if pre.cancelled:
                return
            arg_conv = pre.args

            ret = self.func(**arg_conv)

            post = _events.PostExecutionEvent(self, ret)
            _bus.post(post)

            return ret

    def parser(self, subparser: _argparse._SubParsersAction):
        command_parser = subparser.add_parser(self.command,
                                              help=self.help)
        for k, v in self.arguments.items():
            par, arg = v
            if isinstance(arg, Arg):
                arg.parser(command_parser)

        self.command_parser = command_parser


def task(func=None, *, help=None):
    if func is None:
        return _partial(task, help=help)

    wrapper = Task(func, help if help is not None else '')
    __registry__[wrapper.command] = wrapper
    return wrapper


def taskinfo(task: Task = None, *_, **kwargs):
    if task is None:
        return _partial(taskinfo, **kwargs)

    for k, v in kwargs.items():
        task.__dict__[k] = v

    return task


def run_cmd(program: str, help: str = None):
    pre = _events.ProgramStartedEvent()
    _bus.post(pre)
    if pre.cancelled:
        return

    global __registry__
    main_parser = _argparse.ArgumentParser(
        prog=program, description=help, formatter_class=_argparse.RawTextHelpFormatter)
    subparsers = main_parser.add_subparsers(dest='command')

    for k, registered_task in __registry__.items():
        registered_task.parser(subparsers)

    args = main_parser.parse_args()
    parsed = vars(args)

    if 'command' in parsed:
        command = parsed['command']
        parsed.pop('command')
        if command in __registry__:
            __registry__[command].run(parsed)
        else:
            main_parser.print_help()

    post = _events.ProgramFinishedEvent()
    _bus.post(post)


def run_internal(func: Task, **kwargs):
    return func.run(kwargs)
