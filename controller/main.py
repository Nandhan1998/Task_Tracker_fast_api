from typing import Optional
from fastapi import FastAPI, Query
# import Repository.repository as rp
from Task_Tracker.Repository import repository as rp
from datetime import date
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


@app.post("/create_task")
def create_a_task(
        project_id: int = Query(...,
                                description="ID of the project to which the task belongs"),
        task_name: str = Query(...,
                               description="Name of the task to be created"),
        end_date: int = Query(
            ..., description="Enter the number of days to complete the task from the date of creation"),
        status: Optional[int] = Query(0, description="Status of the task (1=in progress, 2=on hold, 3=completed)")):
    return rp.create_task(project_id,task_name,end_date,status)


