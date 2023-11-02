import click
import pkg_resources
from tm_sl.com import *
from tm_sl.sl import groups, projects, tasks  # Import your core logic functions
from tm_sl.sl.manager import SnapLogicManager  # Import the SnapLogicManager from where it's defined

from tm_sl.cli.project import project
from tm_sl.cli.group import group
from tm_sl.cli.snaplex import snaplex
from tm_sl.cli.migrate import migrate
from tm_sl.cli.task import task
from tm_sl.cli.tenant import tenant
def _entry_point():
    main(obj={})

@click.group()
@click.pass_context
@click.option('--username', '-u', required=False, default = None, help='SnapLogic username')
@click.option('--password', '-p', required=False, default = None, help='SnapLogic password')
@click.option('--env', '-e', required=False, default = None, help='Path to environment file')
def main(ctx, username, password, env):
    """
    Initialize the CLI application with optional SnapLogic credentials and environment file. 
    It sets up the context for subsequent CLI commands to interact with SnapLogic resources.
    
    If nothing is provided, it will try to load the default .env file in the current directory.
    If a .env file can't be found the env variables SL_USER and SL_PASSWORD will be tried.

    Example:
    ```shell
        $ tm-sl --username myuser --password mypass group list tidemark-dev
        $ tm-sl -e ./slcreds.env group list tidemark-dev
        [
            "admins",
            "members",
            "py_test_dev",
            "py_test_run",
            "python_test_group",
            "t_baseline_devs",
            "t_baseline_run"
        ]
    ```
    """
    ctx.obj['manager'] = SnapLogicManager(username, password, env)  # Create a manager object and store it in the context object

@main.command(name='version')
def version_command():
    """Display the current version of the application."""
    # Replace with your actual version
    version = pkg_resources.get_distribution("tm_sl").version
    print(f"tm-sl version: {version}")

main.add_command(group)
main.add_command(project)
main.add_command(snaplex)
main.add_command(migrate)
main.add_command(task)
main.add_command(tenant)

if __name__ == "__main__":
    _entry_point()
