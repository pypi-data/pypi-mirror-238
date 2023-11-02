## DOCSTRINGS SHOULD BE GENEREATED WITHOUT PARAMETERS
## DOCSTRINGS ARE NOT REQUIRED FOR GROUP COMMANDS
## AN EXAMPLE USING THE COMMAND NAME IN THIS FILE ALONG WITH THE SUBCOMMAND IS PREFERABLE
## ```shell
##      $ tm-sl --env sl.env group_command subcommand (options)/(args)
##  ```

import click
from tm_sl.com import *

from tm_sl.sl import projects

@click.group('project', help='Manage projects.')
@click.pass_context
def project(ctx):
    pass  # Here for the purpose of defining a group, no action needed


@project.command('list')
@click.argument('org', required=True)
@click.argument('project_space', required=True)
@click.pass_context
def project_list(ctx, org, project_space):
    """
    List all projects within a specified organization and project space.

    This command retrieves and displays all projects present in the specified organization and project space.

    Example:
    ```shell
        $ tm-sl project list myorg myprojectspace
        [
            {
                "name": "Project1",
                "id": "123",
                "status": "active"
            },
            {
                "name": "Project2",
                "id": "456",
                "status": "inactive"
            }
        ]
    ```
    """
    c_json(projects.get_all_projects(ctx.obj['manager'] , org , project_space)) # Call the core logic function
