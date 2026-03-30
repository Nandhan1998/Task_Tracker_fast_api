from Task_Tracker.db_conn import get_connection


def create_project(project_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO projects (project_name) VALUES (%s) RETURNING pid;"
    cursor.execute(query, (project_name,))

    project_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return {"id": project_id, "project_name": project_name}


def get_all_projects():
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT pid, project_name ,date(project_created_date) FROM projects;"
    cursor.execute(query)

    rows = cursor.fetchall()

    # convert to list of dictionaries
    projects = []
    for row in rows:
        projects.append({
            "pid": row[0],
            "pname": row[1],
            "project_create_date": row[2]
        })

    cursor.close()
    conn.close()

    return projects


def create_a_task(project_id: int,
                  task_name: str,
                  end_date: int,
                  status: int):
    conn = get_connection()
    cursor = conn.cursor()
    query1 = "select pid  from projects"
    cursor.execute(query1)
    rows = cursor.fetchall()

    pid_list = [row[0] for row in rows]
    if project_id in pid_list:
        query = """
            INSERT INTO Task_mast (task_name, status, end_date, project_id)
            VALUES (%s, %s, NOW() + (%s * INTERVAL '1 day'), %s) 
        """
        values = (task_name, status, end_date, project_id)

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": "Task created successfully"}
    else:
        return {"error": "you entered project is not present "}
