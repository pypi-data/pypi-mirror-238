# [Normal]PyRunner

PyRunner allows you to run shell commands from Python in a way similar to how it is happening inside shell scripts

The following features apply:

* you don't think about separation of arguments and command; entire string is executed instead
* you don't think if command is built-in or external
* output of a command to either `stdout` or `stderr` is printed into appropriate stream and visible to user (until muted)
* called command is printed 
* commands can be called with `sudo` and the password for the current user will be asked once
* entire script can be called with `sudo` and the password, asked by sudo command, will be in effect
* the result of a command can be grabbed, including `stdout`, `stderr` and return code

The idea is to completely avoid boilerplate coding when writing shell automation scripts in Python.

# Examples

## Importing library

    >>> import pyrunner

## Calling `ls` command

    >>> _=pyrunner.exec("ls")
    $ 'ls'
    examples.py
    __pycache__
    pyrunner.py
    README.md
    setup.py

Note `_=` is used for Python REPL to suppress result printing.

Note command is printed with `$` prefix.

## Collecting command output as a whole string

    >>> hostname=pyrunner.exec("hostname")
    $ 'hostname'
    myhost
    >>> print(hostname)
    myhost

## Collecting command output as a list of strings

    >>> files = []
    >>> _=pyrunner.exec("ls", out_lines=files)
    $ 'ls'
    mnt
    __pycache__
    pyrunner.py
    README.md
    setup.py
    >>> files
    ['mnt', '__pycache__', 'pyrunner.py', 'README.md', 'setup.py', '']

## Suppressing printouts

    >>> pyrunner.exec("ls", mute_out=True)
    $ 'ls'
    'mnt\n__pycache__\npyrunner.py\nREADME.md\nsetup.py'


## Calling `uname` command with arguments

    >>> _=pyrunner.exec("uname -a")
    $ 'uname -a'
    Linux myhostname 5.15.0-86-generic #96-Ubuntu SMP Wed Sep 20 08:23:49 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux


## Calling sudo command (`mount`)

    >>> _=pyrunner.exec("mount /dev/loop46 mnt", sudo=True)
    $ sudo mount /dev/loop46 mnt
    [sudo] password for myuser:
    mount: /home/myuser/mypath/pyrunner/mnt: WARNING: source write-protected, mounted read-only.

Note `sudo=True` is used to initiate `sudo` operations.

Note command is now prefixed with `$ sudo `

## Checking mount is worked

    >>> _=pyrunner.exec("ls mnt")
    $ 'ls mnt'
    bin
    chromium.png
    etc
    firstrun
    lib
    man1
    meta
    snap
    tests
    usr

showing some image content.

## Unmounting

    >>> _=pyrunner.exec("umount mnt", sudo=True)
    $ sudo umount mnt

Note password is not asked.

# Security notes

Password is stored in Python variable. It is okay with standalone scripts, but can be not okay with interactive shells 
like Jupyter. `sudoers` check is not supported yet.





