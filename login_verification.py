import bcrypt
import users_db


def check_session(username, password):
    users = users_db.get_users()
    for user in users:
        if user['username'] == username and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return True, user['role'], user['id']

    return False, False, False


def check_exist(username, password, actual_user=True):
    users = users_db.get_users()
    new_password = crypt_password(password)

    for user in users:
        if user['username'] != actual_user:
            if user['username'] == username:
                return False, False

        elif password == "" and user['username'] == actual_user:
            new_password = user['password']

    return True, new_password


def crypt_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
