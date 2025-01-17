import sqlite3


class Database():
    def __init__(self):
        self.con = sqlite3.connect('task-database.db')
        self.cursor = self.con.cursor()
        self.create_task_table()

    # Create task table

    def create_task_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tasks (id integer PRIMARY KEY AUTOINCREMENT,  task varchar(50) NOT NULL, due_date varchar(50), completed BOOLEAN NOT NULL CHECK (completedIN (0, 1))")
        self.con.commit()

    # create task
    def create_task(self, task, due_date=None):
        self.cursor.execute(
            'INSERT INTO tasks(task, due_date, completed) VALUES(?, ?, ?)', (task, due_date, 0))
        self.con.commit()

        # Get last entry and add to task list
        created_task = self.cursor.execute(
            'SELECT id, task, due_date FROM tasks WHERE task = ? and completed = 0', (task,)).fetchall()
        return created_task[-1]

    # Get tasks
    def get_tasks(self):
        # Get all tasks completed and uncompleted
        uncompleted_tasks = self.cursor.execute(
            'SELECT id, task, due_date FROM tasks WHERE completed = 0').fetchall()
        completed_tasks = self.cursor.execute(
            'SELECT id, task, due_date FROM tasks WHERE completed = 1').fetchall()
        return completed_tasks, uncompleted_tasks

    # Update tasks
    def mark_task_as_completed(self, taskid):
        # Mark task as completed
        self.cursor.execute(
            'UPDATE tasks SET completed = 1 WHERE id = ?', (taskid,))
        self.con.commit()

    def mark_task_as_uncompleted(self, taskid):
        # Mark task as uncompleted
        self.cursor.execute(
            'UPDATE tasks SET completed = 0 WHERE id = ?', (taskid,))
        self.con.commit()

        # return the task text
        task_text = self.cursor.execute(
            'SELECT tasks FROM tasks WHERE id = ?', (taskid,)).fetchall()
        return task_text[0][0]

    # Deleting task
    def delete_task(self, taskid):
        # Delete task'
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (taskid,))
        self.con.commit()

    # Close connection
    def close_db_connection(self):
        self.con.close()
