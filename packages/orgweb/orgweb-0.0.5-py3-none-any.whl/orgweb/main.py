# [[file:../org/orgweb/main.org::*Imports][Imports:1]]
import os
import time
import typer
from . import __version__
from .container import *
from .monitor import OrgFileChangeHandler
from .org import tangle as org_tangle, detangle as org_detangle, execute as org_execute
from rich import print
from typing import List
from typing_extensions import Annotated
from watchdog.observers import Observer
# Imports:1 ends here

# [[file:../org/orgweb/main.org::*Typer][Typer:1]]
app = typer.Typer()
# Typer:1 ends here

# [[file:../org/orgweb/main.org::*Version Command][Version Command:1]]
@app.command()
def version():
    """Get the current installed version of orgweb"""
    print(f"Version: {__version__}")
# Version Command:1 ends here

# [[file:../org/orgweb/main.org::*Config Command][Config Command:1]]
@app.command()
def config():
    """Get the current configuration of orgweb"""
    # print(f"DOCS_PATH: {os.environ.get('DOCS_PATH')}")
# Config Command:1 ends here

# [[file:../org/orgweb/main.org::*Tangle Command][Tangle Command:2]]
@app.command()
def tangle(folder: str = typer.Argument(..., help="Folder where the Org-mode files to tangle are located"),
           files: Annotated[List[str],
                            typer.Option("--file", help="Optional list of one or more files to tangle from `folder`")] = None):
    """Tangle the org files in the given folder"""
    org_tangle(folder, files)
# Tangle Command:2 ends here

# [[file:../org/orgweb/main.org::*Detangle Command][Detangle Command:2]]
@app.command()
def detangle(folder: str = typer.Argument(..., help="Folder where the source files to detangle are located"),
             files: Annotated[List[str],
                           typer.Option("--file",
                           help="Optional list of one or more files to tangle from `folder`")] = None):
    """Detangle the source files in the given folder"""
    org_detangle(folder, files)
# Detangle Command:2 ends here

# [[file:../org/orgweb/main.org::*Execute Command][Execute Command:2]]
@app.command()
def execute(folder: str = typer.Argument(..., help="Folder where the Org-mode files to execute are located"),
            files: Annotated[List[str],
                            typer.Option("--file",
                            help="Optional list of one or more files to execute from `folder`")] = None):
    """Execute the org files in the given folder"""
    org_execute(folder, files)
# Execute Command:2 ends here

# [[file:../org/orgweb/main.org::*Monitor Command][Monitor Command:1]]
@app.command()
def monitor(folder: str = typer.Argument(..., help="The folder to monitor for changes")):
    """Monitor the given folder for changes and tangle the org files when they change"""
    folder = os.path.expanduser(folder)
    event_handler = OrgFileChangeHandler(folder)
    observer = Observer()
    observer.schedule(event_handler, path=folder, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
# Monitor Command:1 ends here

# [[file:../org/orgweb/main.org::*detect if Docker is running, otherwise return a clean error.][detect if Docker is running, otherwise return a clean error.:1]]
def init():
    """Initialize orgweb"""

    # Make sure the Docker image exists on the local system
    if not image_exists():
        print("Building image...")
        image, logs = build_image()
        print(f"Image built [{image.id}]")

    app()

if __name__ == "__main__":
    init()
# detect if Docker is running, otherwise return a clean error.:1 ends here
