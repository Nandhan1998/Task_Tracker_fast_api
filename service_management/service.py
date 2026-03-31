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


def create_a_task(project_id: int, task_name: str, end_date: int, status: int):
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


def get_all_task(project_id: int):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        projects = []

        query1 = "SELECT pid FROM projects"
        cursor.execute(query1)
        rows = cursor.fetchall()

        pid_list = [row[0] for row in rows]
        print("Available PIDs:", pid_list)

        if project_id != 0 and project_id not in pid_list:
            return {"error": "Entered project id is not present"}

        if project_id == 0:
            query = """ SELECT p.pid, p.project_name, t.task_id, t.task_name, case 
                        when t.status=0 then 'To_do'
                        when t.status=1 then 'in progress'
                        when t.status=2 then 'on hold'
                        when t.status=3 then 'completed' end as status
                FROM projects p ,task_mast t where  t.project_id = p.pid """
            cursor.execute(query)

        else:
            query = """ SELECT p.pid, p.project_name, t.task_id, t.task_name, case 
                        when t.status=0 then 'To_do'
                        when t.status=1 then 'in progress'
                        when t.status=2 then 'on hold'
                        when t.status=3 then 'completed' end as status FROM projects p ,task_mast t where  t.project_id = p.pid and p.pid=%s """
            cursor.execute(query, (project_id,))

        rows = cursor.fetchall()

        if not rows:
            print(" No data found")
            return []

        for row in rows:
            projects.append({
                "project_id": row[0],
                "project_name": row[1],
                "task_id": row[2],
                "task_name": row[3],
                "status": row[4]
            })

        print("Query:", query)
        print("Params:", project_id)

        return projects

    except Exception as e:
        print(" Error occurred:", str(e))
        return {"error": str(e)}

    finally:
        # Always close safely
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_task(task_id: int):
    conn = None
    curr = None
    try:
        conn = get_connection()
        curr = conn.cursor()

        query = "DELETE FROM task_mast WHERE task_id = %s RETURNING task_id"
        curr.execute(query, (task_id,))

        result = curr.fetchone()

        if result is None:
            return {"error": "Task ID not found"}

        conn.commit()

        deleted_task_id = result[0]

        return {"msg": f"Deleted task id is {deleted_task_id}"}

    except Exception as e:
        print("Error occurred:", str(e))
        return {"error": str(e)}

    finally:
        if curr:
            curr.close()
        if conn:
            conn.close()


def update_task(task_id: int, status: int):
    print("service====================\n=========================\n")
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """ update task_mast set status=%s where task_id=%s returning task_id"""

        cursor.execute(query, (status, task_id))

        res = cursor.fetchone()

        conn.commit()
        if res:
            return {"updated_task_id": res[0]}
        else:
            return {"message": "No task found with given task_id"}

    except Exception as e:
        print("exception is ", str(e))
        return {"error :": str(e)}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
