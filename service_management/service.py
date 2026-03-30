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
            "project_create_date":row[2]
        })

    cursor.close()
    conn.close()

    return projects
