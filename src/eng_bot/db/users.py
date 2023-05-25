import psycopg2

from config import dbname, user, password, host

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
cursor = conn.cursor()


def create(user_id):
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
    
    users_id = cursor.fetchone()
    if users_id == None:
        cursor.execute(f"INSERT INTO users VALUES({user_id})")
        conn.commit()

def check_registration(user_id):
    cursor.execute(f"SELECT is_registered FROM users WHERE user_id = {user_id}")
    is_registered = cursor.fetchone()[0]
    return is_registered

def get_first_name(user_id):
    cursor.execute(f"SELECT first_name FROM users WHERE user_id = {user_id}")
    f_name = cursor.fetchone()
    return None if f_name == None else f_name[0]

def get_last_name(user_id):
    cursor.execute(f"SELECT last_name FROM users WHERE user_id = {user_id}")
    l_name = cursor.fetchone()
    return None if l_name == None else l_name[0]

def get_status(user_id):
    cursor.execute(f"SELECT status FROM users WHERE user_id = {user_id}")
    status = cursor.fetchone()
    return None if status == None else status[0]

def get_group(user_id):
    cursor.execute(f"SELECT student_group FROM users WHERE user_id = {user_id}")
    group = cursor.fetchone()
    return None if group == None else group[0]

def get_action(user_id):
    cursor.execute(f"SELECT action FROM users WHERE user_id = {user_id}")
    action = cursor.fetchone()
    return None if action == None else action[0]

def get_selection(user_id):
    cursor.execute(f"SELECT selection FROM users WHERE user_id = {user_id}")
    selection = cursor.fetchone()
    return None if selection == None else selection[0]

def get_user(user_id):
    cursor.execute(f"SELECT user_id, first_name, last_name, status, score, student_group FROM users WHERE user_id = {user_id}")
    temp = cursor.fetchone()
    user = {"user_id": temp[0], "first_name": temp[1], "last_name": temp[2], "status": temp[3], "score": temp[4], "student_group": temp[5]}
    return user

def set_first_name(user_id, f_name):
    if f_name is None:
        cursor.execute(f"UPDATE users SET first_name = NULL WHERE user_id = {user_id}")
    else:
        cursor.execute(f"UPDATE users SET first_name = '{f_name}' WHERE user_id = {user_id}")
    conn.commit()

def set_last_name(user_id, l_name):
    if l_name is None:
        cursor.execute(f"UPDATE users SET last_name = NULL WHERE user_id = {user_id}")
    else:
        cursor.execute(f"UPDATE users SET last_name = '{l_name}' WHERE user_id = {user_id}")
    conn.commit()
    
def set_group(user_id, group):
    if group is None:
        cursor.execute(f"UPDATE users SET student_group = NULL WHERE user_id = {user_id}")
    else:
        cursor.execute(f"UPDATE users SET student_group = '{group}' WHERE user_id = {user_id}")
    conn.commit()

def set_registration(user_id, status):
    cursor.execute(f"UPDATE users SET is_registered = {status} WHERE user_id = {user_id}")
    conn.commit()

def set_action(user_id, action):
    if action == None:
        cursor.execute(f"UPDATE users SET action = NULL WHERE user_id = {user_id}")
    else:
        cursor.execute(f"UPDATE users SET action = '{action}' WHERE user_id = {user_id}")
    conn.commit()

def set_selection(user_id, selection):
    if selection == None:
        cursor.execute(f"UPDATE users SET selection = NULL WHERE user_id = {user_id}")
    else:
        cursor.execute(f"UPDATE users SET selection = '{selection}' WHERE user_id = {user_id}")
    conn.commit()

def add_score(user_id, score):
    cursor.execute(f"UPDATE users SET score = score + {score} WHERE user_id = {user_id}")
    conn.commit()

def get_leader_board_data():
    cursor.execute(f"""
                   SELECT user_id, first_name, last_name, is_registered, score 
                   FROM users 
                   ORDER BY score DESC 
                   LIMIT 10;""")
    
    temp = cursor.fetchall()
    users = [{'user_id': user[0], 'first_name': user[1], 'last_name': user[2], 'is_registered': user[3], 'score': user[4]} for user in temp]
    return users