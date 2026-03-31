from Task_Tracker.service_management import service as sr


def project_creation_service(project_name: str):

    if not project_name or project_name.strip() == "":
        return {"error": "Project name cannot be empty"}

    if len(project_name) < 3:
        return {"error": "Project name must be at least 3 characters"}

    return sr.create_project(project_name)


def see_all_projects():
    return sr.get_all_projects()


def create_task(project_id: int,
                task_name: str,
                end_date: int,
                status: int):
    if project_id < 0:
        return {"error": "enter the project id greater than 0"}

    if task_name.strip() == "" and len(task_name.strip()) < 5:
        return {"error": "entered task name is empty or too sort name"}

    if end_date < 0:
        return {"error": "enter the positive number of days"}
    lis = [0, 1, 2, 3]
    if status not in lis:
        return {"error": "enter the status from 0 to 3"}

    return sr.create_a_task(project_id, task_name, end_date, status)


def get_all_task(project_id: int):
    if project_id < 0:
        return {"error": "enter the project id greater tahn zero"}
    return sr.get_all_task(project_id)


def delete_task(task_id: int):
    if task_id < 0:
        return {"error": "enter the valid task"}
    return sr.delete_task(task_id)


def update_task(task_id: int, status: int):
    print("repository====================\n=========================\n")

    if task_id < 0:
        return {"error": "enterd task id should be greater than 0"}
    if status < 0 or status > 3:
        return {"error": "invalid status"}
    return sr.update_task(task_id, status)
