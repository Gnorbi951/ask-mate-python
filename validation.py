import bcrypt
import data_manager


def hash_password(text_password):
    hashed_bytes = bcrypt.hashpw(text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def check_if_user_name_exists(user_name):
    all_users = data_manager.list_users()
    every_user = []
    for name in all_users:
        every_user.append(name.get('user_name'))
    if user_name in every_user:
        return True
    else:
        return False
