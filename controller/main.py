from fastapi import FastAPI
# import Repository.repository as rp
from Task_Tracker.Repository import repository as rp
app = FastAPI()


@app.get("/")
def welcome():
    return {"message": "welcome to fastapi"}


@app.post("/create_project")
def create_project(project_name: str):
    return rp.project_creation_service(project_name)


@app.get("/get_all_project")
def get_allproject():
    return rp.see_all_projects()
