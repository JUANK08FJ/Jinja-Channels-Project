import sqlite3


def get_users():
    conn = sqlite3.connect("tv_channels.sqlite")
    sql = "SELECT * FROM users;"
    cursor = conn.execute(sql)
    users = []
    for row in cursor:
        user = {"id": row[0], "username": row[1], "password": row[2], "role": row[3]}
        users.append(user)
    conn.close()

    return users


def user_creation(username, password, role):
    conn = sqlite3.connect("tv_channels.sqlite")
    sql = "INSERT INTO users (username, password, admin_role) VALUES (?,?,?)"

    values = [username, password, role]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


def user_deletion(user_id):
    conn = sqlite3.connect("tv_channels.sqlite")
    sql = "DELETE FROM users WHERE user_id == ?"

    values = [user_id]

    conn.execute(sql, values)
    conn.commit()
    conn.close()


def user_modification(id_user, username, password, role):
    conn = sqlite3.connect("tv_channels.sqlite")
    sql = "UPDATE users SET username = ?, password = ?, admin_role = ? WHERE user_id = ?"

    values = [username, password, role, id_user]

    conn.execute(sql, values)
    conn.commit()
    conn.close()
