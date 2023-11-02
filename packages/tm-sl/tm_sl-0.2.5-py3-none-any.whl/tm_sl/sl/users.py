from requests.exceptions import HTTPError

def get_all_users(caller, org):
    """
    Retrieve all users in an org.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's name.

    Returns:
        list: A list of all users in the org.
    """
    path = f"asset/user/settings?path=%2F{org}"
    data, response = caller.r("GET", path)
    users = data['users']
    return users

def get_user(caller, email, org=None):
    """
    Retrieve a user by email. If an organization name is provided, it retrieves the user from that specific org.

    Parameters:
        caller: The object responsible for making HTTP requests.
        email (str): The email of the user to retrieve.
        org (str, optional): The organization's name. Defaults to None.

    Returns:
        dict: A dictionary containing the user's details if found.

    Raises:
        Exception: If the user with the given email is not found in the provided org.

    Example:
        >>> user = get_user(caller, "user@example.com", "exampleOrg")
        >>> print(user)
        {'username': 'user@example.com', 'roles': ['admin'], 'status': 'active'}
    """
    if org != None:
        users = get_all_users(caller, org)
        for user in users:
            if user['username'] == email:
                return user
        return None
    path = f"asset/user/{email}"
    data, response = caller.r("GET", path)
    return data

def get_user2(caller, email, org):

    path = f"asset/user/{email}/org/{org}"
    try:
        data, response = caller.r("GET", path)
        return data
    except HTTPError as e:
        if e.response.status_code == 404:
            return None

def create_user(caller, org, email , ip=True):
    """
    Create a new user in a specific organization.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's name where the user will be created.
        email (str): The email of the user to create.
        ip (bool, optional): Intelligent Playform access. Defaults to True.
    Example:
        >>> create_user(caller, "exampleOrg", "newuser@example.com")
        # User 'newuser@example.com' is now created in 'exampleOrg'
    """

    data, response = caller.r(
                            "PUT", 
                            f"asset/user/{email}/org/{org}", 
                            json={"create_home_directory":False}
                            )

 
    payload = {
        "org_path": org,
        "users": [
            {
                "app_access": {
                    "intelligent_integration_platform": ip
                },
                "username": email
            }
        ]
    }
    data, response = caller.r(
                            "POST", 
                            f"asset/user/app_access", 
                            json=payload, 
                            headers={'Content-Type': 'application/json'}
                            )
    if ip:
        data, response = caller.r(
                            "POST", 
                            f"asset/user/app_access", 
                            json=payload, 
                            headers={'Content-Type': 'application/json'}
                            )
        
def delete_user(caller, org, email):
    """
    Delete a user from a specific organization.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's name from which the user will be deleted.
        email (str): The email of the user to delete.

    Example:
        >>> delete_user(caller, "exampleOrg", "user@example.com")
        # User 'user@example.com' is now deleted from 'exampleOrg'
    """
    path = f"asset/user/{email}/org/{org}"
    data, response = caller.r("DELETE", path)
