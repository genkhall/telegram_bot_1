import random
import sqlite3


def sql_create():
    global db, cursor
    db = sqlite3.connect("mentorss.db")
    cursor = db.cursor()

    if db:
        print("База готова!")

    db.execute(
        "CREATE TABLE IF NOT EXISTS mentors "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "id_from_user INTEGER, "
        "name VARCHAR (50), "
        "direction VARCHAR (20), "
        "age INTEGER, "
        "mentor_group VARCHAR(10))"

    )
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as FSMCONTEXT_PROXY_STORAGE:
        cursor.execute("INSERT INTO mentors VALUES"
                       "(null, ?, ?, ?, ?, ?)", tuple(FSMCONTEXT_PROXY_STORAGE.values()))
        db.commit()


async def sql_command_random():
    users = cursor.execute("SELECT * FROM mentors").fetchall()
    random_user = random.choice(users)
    return random_user


async def sql_command_all():
    return cursor.execute("SELECT * FROM mentors").fetchall()


async def sql_command_delete():
    cursor.execute("DELETE FROM mentors WHERE id == ?", (id,))

    db.commit()


sql_create()
