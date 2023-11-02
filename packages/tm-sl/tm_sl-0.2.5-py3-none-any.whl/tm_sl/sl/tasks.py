from tm_sl.com import *

def get_all_tasks(caller, org, project_space, project_name):
    """
    Get all tasks in a project.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's ID.
        project_space (str): The project space's ID.
        project_name (str): The project's name.

    Returns:
        list: A list of all tasks within the specified project.

    Example:
    ```python
        from tm_sl.sl import tasks as t
        data, response = get_all_tasks(caller, 'myorg', 'myspace', 'myproject')
        print(data)
        # Output: [{'id': '123', 'name': 'task1'}, {'id': '456', 'name': 'task2'}, ...]
    ```
    """
    path = f"asset/list/{org}/{project_space}/{project_name}?asset_type=Job&limit=1000&offset=0&sort=c_time:-1&search="
    data, response = caller.r("GET", path)
    return data['entries']

def get_task_config(caller, snode_id):
    """
    Get the configuration of a task.

    Parameters:
        caller: The object responsible for making HTTP requests.
        snode_id (str): The task's ID.

    Returns:
        dict: The configuration data of the specified task.

    Example:
    ```python
        from tm_sl.sl import tasks as t
        data, response = t.get_task_config(caller, 'ase1234123s123')
        print(data)
        # Output: {'id': '123', 'name': 'task1', 'config': {...}}
    ```
    """
    path = f"slsched/job/{snode_id}?include_rbin=true"
    data, response = caller.r("GET", path)
    return data

def change_snaplex_task(caller, org, snode_id, splex_name):
    """
    Change the snaplex of a task.

    Parameters:
        caller: The object responsible for making HTTP requests.
        org (str): The organization's ID.
        snode_id (str): The task's ID.
        splex_name (str): The name of the snaplex.

    Returns:
        dict: The response data after changing the snaplex of the task.

    Example:
    ```python
        from tm_sl.sl import tasks as t
        data, response = t.change_snaplex_task(caller, 'myorg', '123', 'new_snaplex')
        print(data)
    ```
    """
    task = get_task_config(caller, snode_id)
    try: rtpath = task['parameters']['runtime_path_id']
    except: rtpath = None
    try: tstatus = task['parameters']['enabled']
    except: tstatus = None

    if rtpath == None or rtpath != (org + '/rt/sidekick/'+ splex_name):
        change_one = f"https://elastic.snaplogic.com/api/1/rest/"
        task['parameters']['runtime_path_id'] = org + '/rt/sidekick/'+ splex_name
        if tstatus == None or tstatus != True:
            task['parameters']['enabled'] = True
        # filtered['parameters']['path'] = "/tidemark-us/shared/test"
        data, response = caller.r('PUT', f"slsched/job/{task['snode_id']}?duplicate_check=True" , json=task)
        return data
