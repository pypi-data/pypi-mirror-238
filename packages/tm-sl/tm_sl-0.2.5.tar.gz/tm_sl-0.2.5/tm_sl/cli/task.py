import click
from tm_sl.com import *

from tm_sl.sl import tasks as t

@click.group('task', help='Manage Tasks.')
@click.pass_context
def task(ctx):
    pass  # Here for the purpose of defining a group, no action needed


@task.command('get_all', help='List all tasks.')
@click.option('--path','-p', required=True, help= "Snaplogic path in the form of org/project_space/project_name")
@click.pass_context
def get_all(ctx, path):
    """
    List all projects.

    This command retrieves and displays all tasks present in the specified Snaplogic path.

    Example:
    ```shell
        $ tm-cli task get_all --path org/project_space/project_name
        [
            "task1",
            "task2",
            "task3"
        ]
    ```
    """
    c_json(t.get_all_tasks(ctx.obj['manager'] , *path.split("/")))

def get_task_config(ctx, path):
    pass

@task.command('fix_all', help='Change the snaplex on all tasks')
@click.option('--path','-p', required=True, help= "Snaplogic path in the form of org/project_space/project_name")
@click.option('--snaplex','-s', required=True, help= "Snaplex name in the 'environment' field of the snaplex config")
@click.pass_context
def fix_all(ctx, path, snaplex):
    """
    Fix all tasks to a new snaplex.

    This command changes the snaplex on all tasks present in the specified Snaplogic path to a new snaplex.

    Example:
    ```shell
        $ tm-sl task fix_all --path org/project_space/project_name --snaplex new_snaplex
        "All tasks have been updated to use the new_snaplex snaplex."
    ```
    """
    org, ps, project = path.split("/")
    data = t.get_all_tasks(ctx.obj['manager'] , *path.split("/") )
    for task in data:
        t.change_snaplex_task(ctx.obj['manager'] , org, task['snode_id'], snaplex)
    