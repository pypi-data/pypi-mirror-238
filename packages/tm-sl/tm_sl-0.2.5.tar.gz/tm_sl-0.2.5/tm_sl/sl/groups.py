def get_all_groups(caller, org):
    """
    Retrieve all groups within a specified organization.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's ID.

    Returns:
        list: A list of all groups within the specified organization.
    """
    path = f"asset/group/org/{org}"
    data, response = caller.r("GET", path)
    return data

def get_all_users_in_group(caller, org, group):
    """
    Retrieve all users within a specified group and organization.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's ID.
        group (str): The group's ID.

    Returns:
        list: A list of all users within the specified group and organization.
    """
    path = f"asset/group/{group}/org/{org}"
    data, response = caller.r("GET", path)
    return data

def create_group(caller, org, group):
    """
    Create a new group within a specified organization.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's ID.
        group (str): The name of the new group to be created.

    Returns:
        dict: The response data after creating the new group.
    """
    path = f"asset/group/org/{org}"
    data = {"groupname": f"{group}", "members": []}
    data, response = caller.r("POST", path, json=data , headers={'Content-Type': 'application/json'})
    return data

def delete_group(caller, org, group):
    """
    Delete a specified group within an organization.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's ID.
        group (str): The ID of the group to be deleted.

    Returns:
        dict: The response data after deleting the group.
    """
    path = f"asset/group/{group}/org/{org}"
    data, response = caller.r("DELETE", path)
    return data

def add_users_to_group(caller, org, group, users=[]):
    """
    Add a list of users to a specified group within an organization.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's ID.
        group (str): The group's ID.
        users (list, optional): A list of user IDs to be added to the group. Defaults to an empty list.

    Returns:
        dict: The response data after adding users to the group.

    Raises:
        AssertionError: If the users parameter is not a list or is an empty list.
    """
    assert type(users) == list, "Users must be a list"
    assert len(users) > 0, "Users must be a list of length > 0"
    group_users = get_all_users_in_group(caller, org, group)['members']
    for user in users:
        if user not in group_users:
            group_users.append(user)

    path = f"asset/group/{group}/org/{org}"
    data, response = caller.r("PUT", path, json={"members": group_users}, headers={'Content-Type': 'application/json'})
    return data

def overwrite_users_to_group(caller, org, group, users):
    """
    Overwrite the list of users in a specified group within an organization.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's ID.
        group (str): The group's ID.
        users (list): A new list of user IDs to overwrite the existing users in the group.

    Returns:
        dict: The response data after overwriting users in the group.
    """
    path = f"asset/group/{group}/org/{org}"
    data, response = caller.r("PUT", path, json={"members": users}, headers={'Content-Type': 'application/json'})
    return data
