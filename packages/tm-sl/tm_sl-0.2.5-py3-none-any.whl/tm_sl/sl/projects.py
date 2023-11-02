

def get_all_projects(caller, org, project_space):
    """
    Retrieve all projects within a specific organization and project space.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's name.
        project_space (str): The name of the project space.

    Returns:
        list: A list of all projects in the specified organization and project space.
    """
    path = f"asset/list/{org}/{project_space}?limit=100&offset=0&sort=c_time%3A-1&search="
    data, response = caller.r("GET", path)
    return data['entries']

def get_project(caller, org, project_space, project_name):
    """
    Retrieve the data of a specific project within an organization and project space.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's name.
        project_space (str): The name of the project space.
        project_name (str): The name of the project.

    Returns:
        dict: The data of the specified project.
    """
    path = f"asset/{org}/{project_space}/{project_name}"
    data, response = caller.r("GET", path)
    return data

def create_project(caller, org, project_space, project_name):
    """
    Create a new project within a specific organization and project space.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's name.
        project_space (str): The name of the project space.
        project_name (str): The name of the project to be created.

    Returns:
        dict: The data of the newly created project.
    """
    path = f"asset/{org}/{project_space}/{project_name}"
    payload = {
        "asset_type": "Dir",
        "metadata": {
            "pattern": False,
            "validation": True
        },
        "name": project_name
    }
    data, response = caller.r("POST", path, json=payload, headers={'Content-Type': 'application/json'})
    return data

def delete_project(caller, org, project_space, project_name):
    """
    Delete a specific project within an organization and project space.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's name.
        project_space (str): The name of the project space.
        project_name (str): The name of the project to be deleted.

    Returns:
        dict: The data response after the project is deleted.
    """
    path = f"asset/{org}/{project_space}/{project_name}?soft_delete=True&asset_type=Dir"
    data, response = caller.r("DELETE", path)
    return data


def get_project_space(caller, org, project_space):
    """
    Retrieve the data of a specific project space within an organization.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's name.
        project_space (str): The name of the project space.

    Returns:
        dict: The data of the specified project space.
    """

    path = f"asset/{org}/{project_space}"
    data, response = caller.r("GET", path)
    return data

def set_acl(caller, sl_path, subject, role='read', inherit=False, mock=False):
    """
    Set the ACL (Access Control List) for a specified path and subject.

    Parameters:
        caller: The object responsible for making HTTP requests.
        sl_path (str): The path of the asset.
        subject (str): The subject (user or group).
        role (str, optional): The role to be assigned. Defaults to 'read'.
        inherit (bool, optional): Indicates if permissions should be inherited. Defaults to False.
        mock (bool, optional): Indicates if this should be a mock call. Defaults to False.

    Returns:
        None: Sets the ACL for the specified path and subject.
    """

    path = f"asset/acl/{sl_path}"
    
    perms = ["R", "X"]
    if role == 'admin':
        perms = ["R", "W", "X"]
    
    subject_type = "GROUP"
    if "@" in subject:
        subject_type = "USER"
    
    body = {
        "perms": perms,
        "path": f"/{sl_path}",
        "subject": subject,
        "subject_type": subject_type,
        "inherit": inherit
    }
    if mock:
        del body['path']
        return body
    else:
        caller.r("POST", path, json=body, headers={'Content-Type': 'application/json'})


def delete_acl(caller, sl_path, subject):
    """
    Delete the ACL (Access Control List) for a specified path and subject.

    Parameters:
        caller: The object responsible for making HTTP requests.
        sl_path (str): The path of the asset.
        subject (str): The subject (user or group).

    Returns:
        None: Deletes the ACL for the specified path and subject.
    """

    subject_type = "GROUP"
    if "@" in subject:
        subject_type = "USER"
    path = f"asset/acl/{sl_path}"
    query_params = {
        "subject": subject,
        "subject_type": subject_type
    }
    
    caller.r("DELETE", path, query=query_params)

def add_subject_to_project(caller, org, project_space, project_name, subject, ps_role , p_role ):
    """
    Update the ACLs (Access Control Lists) for the project space, project, and shared project to add or update permissions for the specified subject.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's name.
        project_space (str): The name of the project space.
        project_name (str): The name of the project.
        subject (str): The subject (user or group).
        ps_role (str): The role to be assigned at the project space level.
        p_role (str): The role to be assigned at the project level.

    Returns:
        None: Updates the ACLs for the project space, project, and shared project.
    """
    
    project_space_data = get_project_space(caller, org , project_space)
    project_space_acl = project_space_data['acl']
    project_space_owner = project_space_data['owner']

    project_data = get_project(caller, org, project_space, project_name)
    project_acl = project_data['acl']
    project_owner = project_data['owner']
    
    shared_project_data = get_project(caller, org, project_space, "shared")
    shared_project_acl = shared_project_data['acl']
    shared_project_owner = shared_project_data['owner']

    ## first we do project spaces acl rec
    existing_ps_acl = [acl for acl in project_space_acl if acl['subject'] == subject]
    if len(existing_ps_acl) == 0:
        set_acl(caller, f"{org}/{project_space}", subject, role=ps_role, inherit=False)
    else:
        existing_ps_acl = existing_ps_acl[0]
        existing_ps_acl['perms'].sort()
        generated_acl = set_acl(caller, f"{org}/{project_space}", subject, role=ps_role, inherit=False, mock=True)
        generated_acl['perms'].sort() #type: ignore
        if generated_acl != existing_ps_acl:
            set_acl(caller, f"{org}/{project_space}", subject, role=ps_role, inherit=False)


    ## then we do project acl rec
    existing_p_acl = [acl for acl in project_acl if acl['subject'] == subject]
    if len(existing_p_acl) == 0:
        set_acl(caller, f"{org}/{project_space}/{project_name}", subject, role=p_role, inherit=True)
    else:
        existing_p_acl = existing_p_acl[0]
        existing_p_acl['perms'].sort()
        generated_acl = set_acl(caller, f"{org}/{project_space}/{project_name}", subject, role=p_role, inherit=True, mock=True)
        generated_acl['perms'].sort() #type: ignore
        if generated_acl != existing_p_acl:
            set_acl(caller, f"{org}/{project_space}/{project_name}", subject, role=p_role, inherit=True)

    ## Finally, we check the shared project ACL
    existing_shared_acl = [acl for acl in shared_project_acl if acl['subject'] == subject]
    if len(existing_shared_acl) == 0:
        set_acl(caller, f"{org}/{project_space}/shared", subject, role=ps_role, inherit=True)
    else:
        existing_shared_acl = existing_shared_acl[0]
        existing_shared_acl['perms'].sort()
        shared_generated_acl = set_acl(caller, f"{org}/{project_space}/shared", subject, role=ps_role, inherit=True, mock=True)
        shared_generated_acl['perms'].sort() #type: ignore
        if shared_generated_acl != existing_shared_acl:
            set_acl(caller, f"{org}/{project_space}/shared", subject, role=ps_role, inherit=True)


