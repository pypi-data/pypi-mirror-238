## DOCSTRINGS SHOULD BE GENEREATED WITHOUT PARAMETERS
## DOCSTRINGS ARE NOT REQUIRED FOR GROUP COMMANDS
## AN EXAMPLE USING THE COMMAND NAME IN THIS FILE ALONG WITH THE SUBCOMMAND IS PREFERABLE
## ```shell
##      $ tm-sl --env sl.env group_command subcommand (options)/(args)
##  ```

import click
from tm_sl.com import *

from tm_sl.sl import migration as m




@click.command('migrate', help='Migrate using the v1 API')
@click.option('--src','-s', required=True, help='Source project path in the form of org/project_space/project_name')
@click.option('--dst','-d', required=True, help='Destination project path in the form of org/project_space/project_name')
@click.option('--tasks', '-t', is_flag=True, help='Flag to include tasks in the migration')
@click.option('--pipelines', '-p', is_flag=True, help='Flag to include pipelines in the migration')
@click.option('--files', '-f', is_flag=True, help='Flag to include files in the migration')
@click.option('--accounts', '-a', is_flag=True, help='Flag to include accounts in the migration')
@click.option('--wait', '-w', is_flag=True, help='Follow and wait for the migration to complete')
@click.pass_context
def migrate(ctx, src, dst, tasks, pipelines, files, accounts, wait):
    """
    Migrate assets using the v1 API.

    This command migrates specified types of assets from the source project to the destination project.

    Example:
    ```shell
        $ tm-sl migrate --src myorg/myspace/myproject --dst myorg2/myspace2/myproject2 --tasks --pipelines --wait
        "Migration started. Waiting for completion..."
        "Migration completed successfully."
    ```

    Raises:
        AssertionError: If no asset type is specified for migration.
    """
    assets = []
    if tasks: assets.append("Job")
    if pipelines: assets.append("Pipeline")
    if files: assets.append("File")
    if accounts: assets.append("Account")
    assert len(assets) > 0, "At least one asset type must be specified"

    m.migrate(ctx.obj['manager'] , src, dst, asset_types=assets ,follow=wait)
