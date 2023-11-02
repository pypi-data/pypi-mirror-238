from tm_sl.com import *
from time import sleep
import re

def validate_project_path(path):
    """
    Validate the format of a project path.

    Args:
        path (str): The project path to be validated.

    Raises:
        ValueError: If the project path has an invalid format.
    """
    pattern = re.compile(r'^[\w-]+/[\w-]+/[\w-]+$')
    if not pattern.match(path):
        raise ValueError(f"Invalid project path format: {path}. Expected format is org/project_space/project_name.")



def migrate(caller, src_path , dst_path, asset_types=["Pipeline","Job"], follow=True):
    """
    Migrate assets from one project to another.

    Args:
        caller: The caller object for making API requests.
        src_path (str): The source path of the project to migrate from.
        dst_path (str): The destination path of the project to migrate to.
        asset_types (list, optional): A list of asset types to migrate. Defaults to ["Pipeline","Job"].
        follow (bool, optional): Whether to wait for the migration to complete. Defaults to True.

    Returns:
        dict: The response data from the migration request.
    """


    validate_project_path(src_path)
    validate_project_path(dst_path)

    all_assets = ["Account","Pipeline","Job","File"]
    assert all([x in all_assets for x in asset_types]), f"asset_types must be a subset of {all_assets}"


    path = "public/project/migrate/"+src_path
    payload={
        "dest_path":"/"+dst_path,
        "asset_types":asset_types,
        "async_mode": True,
        "duplicate_check":"false"}
    print(f"[bold blue]Migrating [/bold blue]")
    c_json(asset_types)
    print(f"[blue]from: [/blue]{src_path}")
    print(f"[blue]to:   [/blue]{dst_path}")

    data, response = caller.r("POST", path, json=payload, headers={'Content-Type': 'application/json'})
    c_json(data)

    if follow:
        print(f"[dark_orange]Follow was selected, waiting for migration to complete[/dark_orange]")
        fpath = data['status_url'].replace('https://elastic.snaplogic.com/api/1/rest/', '')
        counter = 0
        # print(caller.r("GET", fpath))
        with console.status("[bold green]Migrating...[/bold green]", spinner="dots"):
            while caller.r("GET", fpath)[0]['status'] == 'Started':
                sleep(10)
                counter += 1
                if counter > 220: break
        print(f"[bold green]Migration reported as completed[/bold green]")
    else:
        print(f"[bold blue]Follow was not selected, migration will complete asyncronously[/bold blue]")
    return data
