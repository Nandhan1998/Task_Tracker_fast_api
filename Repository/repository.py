from Task_Tracker.service_management import service as sr


def project_creation_service(project_name: str):

    
    if not project_name or project_name.strip() == "":
        return {"error": "Project name cannot be empty"}

    if len(project_name) < 3:
        return {"error": "Project name must be at least 3 characters"}

    # ✅ call service
    return sr.create_project(project_name)

def see_all_projects():
    return sr.get_all_projects()