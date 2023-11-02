
import click
from tm_sl.com import *

from tm_sl.sl import groups, users

@click.group('group')
@click.pass_context
def group(ctx):
    '''
    Manage groups.
    '''
    pass


@group.command('list')
@click.argument('org', required=True)
@click.pass_context
def list_groups(ctx, org):
    """
    List all groups within the specified organization. 
    It retrieves all the groups in an organization and pretty prints them to the console.

    Example:
    ```shell
        $ tm-sl group list tidemark-dev
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
    c_json(groups.get_all_groups( ctx.obj['manager'], org))

@group.command('add-user')
@click.argument('org', required=True)
@click.argument('email', required=True)
@click.argument('group_name', required=True)
@click.option('--ip', required=False, is_flag=True, help="Add user to IntelligentPlatform")
@click.pass_context
def add_user(ctx, org, email, group_name, ip):
    """
    Add a user to a group.

    Args:
        ctx (Context): The click Context object.
        org (str): The organization to add the user to.
        email (str): The email address of the user to add.
        group_name (str): The name of the group to add the user to.
        ip (bool): Flag indicating whether to add the user to IntelligentPlatform.

    Returns:
        None

    Raises:
        None
    """
    m = ctx.obj['manager']
    if users.get_user(m, email , org):
        print(f"User {email} already exists")
    else:
        users.create_user(m, org, email)
        print(f"Created user {email}") 

    if email not in groups.get_all_users_in_group(m, org, group_name)['members']:
        groups.add_users_to_group(m, org, group_name, [email])

