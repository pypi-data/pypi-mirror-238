from tm_sl.sl import groups, projects


def add_tmgroup_to_project(caller, org, project_space, project_name, group ):
    """
    Adds a team group to a project.

    Args:
        caller (str): The caller of the function.
        org (str): The organization name.
        project_space (str): The project space.
        project_name (str): The project name.
        group (str): The team group.

    Raises:
        UnknownError: If an unknown error occurs.

    Returns:
        None
    """
    groups_data = groups.get_all_groups(caller, org)


    subjects = [{'name': f"t_{group}_dev" , 'role': "admin"},{'name': f"t_{group}_run" , 'role': "read"}]
    missing_subjects = []
    for subject in subjects:
        if subject['name'] not in groups_data:
            missing_subjects.append(subject['name'])
    if len(missing_subjects) > 0:
        for s in missing_subjects:
            groups.create_group(caller, org, s)

    for s in subjects:
        projects.add_subject_to_project(caller, org, project_space, project_name, s['name'], 'read', s['role'])
