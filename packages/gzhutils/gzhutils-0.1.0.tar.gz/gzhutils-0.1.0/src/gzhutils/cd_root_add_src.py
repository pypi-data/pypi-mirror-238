"""
NOTE: importing this module will cause the change of current directory
and python search path.
USE WITH CARE.
"""
import os
import sys
from pathlib import Path


_initialized = False


def cd_project_root() -> Path:
    """
    Change the current working directory to the project root.
    This is accomplished through repeatedly running
    ```
    cd ..
    ```
    until we have found the root directory of current project.

    What identifies a project root? We are looking for the below two entries:
    - src/
    - .git/

    If both are present, then we assume that this is the project root.

    This utility function is useful when we are running a jupyter notebook
    in JupyterLab and we expect the current working directory to be the 
    project root.
    """
    cwd = Path.cwd()
    print("CWD Before changing:", cwd)
    found = False
    while not found:
        iter = filter(
            lambda x: x.name in ('src', '.git'), 
            cwd.glob('*')
        )
        try:
            next(iter); next(iter)
        except StopIteration:
            cwd = cwd.parent
        else:
            found = True

    os.chdir(cwd)
    print("CWD After changing:", cwd)

    return cwd

if not _initialized:
    root = cd_project_root()
    sys.path.append(str(root / 'src'))
