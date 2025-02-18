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


def get_todo_yearly_statistics():
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""select 2 + 3;""")
        queryset = dict_fetchall(cursor)
        return queryset
