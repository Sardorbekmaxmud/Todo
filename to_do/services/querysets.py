from contextlib import closing
from django.db import connection


def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    else:
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def get_todo_by_id(todo_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""select to_do_todo.body, to_do_todo.created_at , 
        to_do_todo.updated_at, auth_user.username, to_do_todohistory.status from to_do_todo 
        inner join auth_user on to_do_todo.author_id = auth_user.id
        left join to_do_todohistory on to_do_todo.id = to_do_todohistory.todo_id
        where to_do_todo.id = {todo_id};""")
        queryset = dict_fetchone(cursor)
        return queryset
