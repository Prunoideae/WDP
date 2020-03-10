# Workflow Descriptor for Python (WDP)

This is a simple framework for setting up Workflow and Tasks, in certain ways, to modularize and simplify several programs that requires an ordered call of several task. Mainly for tools that I'm planned to develop in future.

## 0. What is it doing

WDP implemented several classes and decorators, to setup a pythonic way to add `Task`, a representation of certain process, and `Workflow`, a combination of serveral tasks, to execute certain tasks subsequently, and output a final result. A simple example of `Task` implementation is as below :

```python
from wdp.task import Arg, task, run_cmd

@task(help = 'Some example')
def some(arg1 : str = Arg(name='input')):
    print(arg1)

if __name__ == "__main__":
    run_cmd(program='Hello', help='First task!')
```

When you run this as python file you will get some nice output:

```text
usage: Hello [-h] {some} ...

First task!

positional arguments:
  {some}
    some      Some example

optional arguments:
  -h, --help  show this help message and exit
```

If run with `some` subcommand and `--help` or `-h` flag, you will get some other info:

```text
usage: Hello some [-h] [--input <STR>]

optional arguments:
  -h, --help     show this help message and exit
  --input <STR>
```

Very nice, isn't it?
