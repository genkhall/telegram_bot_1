from database.bot_db import sql_command_all_users


def get_ids_from_users(users: list):
    lst = []
    for user in users:
        lst.append(user[0])
    return lst
