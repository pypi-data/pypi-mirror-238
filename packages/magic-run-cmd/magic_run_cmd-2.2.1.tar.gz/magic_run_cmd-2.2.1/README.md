# Magic Run Command

This provide a clean way to express scripts inside your python code.
The run engine will be shell by default.
This will allow you to run shell scripts from your python code.
```python
from magic_cmd.script import Script

cmd = Script('''
        ls
        touch test.py
        ls
        rm test.py
        ''')
restults:list[str] = cmd()
```

## Installation:

### pip

You can install it via pip:

```
pip install magic-run-cmd
```
### poetry

To install this code, you will need to first install Poetry (https://python-poetry.org/docs/#installation). Poetry is a dependency manager for Python that will allow you to easily install this code and its dependencies.

Once you have Poetry installed, you can install this code by running the following command from the root directory of this code:

```
poetry add magic-run-cmd
```

This will install this code and all of its dependencies.

# Usage:

To run a simple shell command you can use run_cmd.
This is what the shell engine uses under the hood:

```python
from magic_cmd.run_cmd import run_cmd

print(run_cmd('ls'))

output:
LICENSE  README.md  log/  poetry.lock  pyproject.toml  run_cmd/
```

Then, you can call the run_cmd function with a shell command as a string:


If an error thrown it caught, and logged before, erroring out.

You can also specify whether you want the output to be returned as a list or a string:

run_cmd('ls', split=True)

This will output the result as a list, with each element being one line of output.

# Script
Scripts allow you express you script inside your python code inside triple quote.
The extra white spaces are removed so format as needed.
Scripts can be append using append(str).
Or you can add str or other Scripts.
Since the scripts are callable,
to run a script just call its name followed by ().


```python
        script = Scripts('''
        echo "This is a line"
        echo "The white space are ignored"
        ''')
        script()
        script += 'echo "you can add string"'
        script += Script('echo "or another Script"')
        script.append("And you can append too")
        script()
        #[
        # This is a line,
        #The white space are ignored,
        #you can add string,
        #or another Script
        #And you can append too,
        #]
        #Write to a file and return the path
        shell_script:Path = script.writefile(name="shell.sh")
```
