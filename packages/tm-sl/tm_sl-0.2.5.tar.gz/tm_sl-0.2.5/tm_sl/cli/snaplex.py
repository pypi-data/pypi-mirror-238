import click
from tm_sl.com import *

from tm_sl.sl import snaplexes as s

@click.group('snaplex')
@click.pass_context
def snaplex(ctx):
    '''
    Manage Snaplexes.
    '''
    pass  # Here for the purpose of defining a group, no action needed


@snaplex.command('list')
@click.argument('org', required=True)
@click.pass_context
def snaplex_list(ctx, org):
    """
    List all Snaplexes in a specified organization.

    This command retrieves and displays all Snaplexes present in the specified organization.

    Example:
    ```shell
        $ tm-sl snaplex get_all myorg
        [
            {
                "name": "Snaplex1",
                "id": "123",
                "status": "active"
            },
            {
                "name": "Snaplex2",
                "id": "456",
                "status": "inactive"
            }
        ]
    ```
    """
    c_json(s.get_all_splex_data(ctx.obj['manager'] , org))

@snaplex.command('binary')
@click.option('--path','-p', required=True, help="Snaplex path in the form of org/project_space/project_name/snaplex_name")
@click.option('--savepath','-s', required=True, help="Filepath to save the snaplex binary to (must end with .slpropz)")
@click.pass_context
def snaplex_binary(ctx, path, savepath):
    """
    Downloads a binary config of the specified snaplex to the specified filepath.
    """
    s.get_splex_binary(ctx.obj['manager'] , path, savepath)