
def get_all_splex_data(caller, org):
    """
    Get all the data related to Splex for a specific organization.

    Args:
        caller: An object providing the API call functionality.
        org (str): The name of the organization.

    Returns:
        dict: The data related to Splex for the specified organization.
    """
    path = f"plex/org/{org}"
    data, response = caller.r("GET", path)
    return data

def list_all_splex_in_project(caller, project_path):
    '''
    path: org/space/project
    '''
    path = f"asset/list/{project_path}?asset_type=Plex&limit=100&offset=0&sort=c_time%3A-1&search="
    data, response = caller.r("GET", path)
    return data['entries']

def get_splex_binary(caller, sl_path, save_path=None): ## maybe refactor to just get binary data
    """
    Downloads the binary data for a specified snaplex.

    Args:
        caller: The caller object.
        sl_path (str): The path to the snaplex e.g "tidemark-dev/shared/dev1".
        save_path (str, optional): The path to save the downloaded binary data. Default is None.

    Raises:
        AssertionError: If save_path is None or does not end with ".slpropz".

    Returns:
        None
    """
    
    assert save_path != None or save_path.endswith(".slpropz"), "save_path must not be None or end with .slpropz"
    path = f"plex/links/{sl_path}"
    data, response = caller.r("GET", path)
    snap_config_url = data['config']
    caller.download_binary(snap_config_url, save_path)
