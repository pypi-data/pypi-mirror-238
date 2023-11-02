
import click
from tm_sl.com import *

from tm_sl.sl import groups, tenants, projects

@click.group('tenant')
@click.pass_context
def tenant(ctx):
    """
    Manage snaplogic functions for the Tidemark application.
    These bindings will include tenant specific combos.
    """
    pass



@tenant.command('prep')
@click.option('--path',"-p", required=True, help="SLPath to the project org/project_space/project")
@click.option('--tenant',"-t", required=True, help="tidemark tenant name e.g. 'teslamotors'")
@click.pass_context
def assert_project_group(ctx, path, tenant):
    """
    Prepares a project, group, and permissions for a tenant.

    1) Create a project if it does not already exist
    2) Create the group if it does not already exist
    3) Add the group to the project if it is not already added and reconciles permissions
    4) Add the group to the project space as well as the shared project in the selected project space

    """
    
    org, project_space, project_name = path.split('/')
    all_projects = projects.get_all_projects(ctx.obj['manager'], org, project_space)
    if project_name not in [project['name'] for project in all_projects]:
        print("[bold blue]Project does not exist, creating...[/bold blue]")
        projects.create_project(ctx.obj['manager'], org, project_space, project_name)
    tenants.add_tmgroup_to_project(ctx.obj['manager'], org, project_space, project_name, tenant)

