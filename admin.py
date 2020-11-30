import sqlite3

con = sqlite3.connect('users_db.sqlite')

cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
                id INT,
                flag INT
            )""")

cur2 = con.cursor()
cur2.execute("""CREATE TABLE IF NOT EXISTS posts(
                id INT,                
                sendText TEXT,
                minute INT,
                hour INT,
                day INT,
                month INT
                year INT,
                flag INT
            )""")

def select_user(id):
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("SELECT * FROM users WHERE id=?", (id,))
    result = cur.fetchone()

    con.close()

    return result

def select_users_all():
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("SELECT * FROM users")
    result = cur.fetchall()

    con.close()

    return result


def select_post():
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("SELECT * FROM posts")
    result_post = cur.fetchone()

    con.close()

    return result_post

def select_post_flag(flag):
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("SELECT * FROM posts WHERE flag = ?", (flag,))
    result_post = cur.fetchone()

    con.close()

    return result_post

def create_user(id):
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("INSERT INTO users values (?, 0)", (id,))

    con.commit()
    con.close()

def create_post(id, text):
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("INSERT INTO posts values (?, ?, 0, 0, 0, 0, 0, 0)", (id, text))

    con.commit()
    con.close()

def update_user_flag(id, flag):
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("""UPDATE users SET flag = ? WHERE id = ?""", (flag, id))

    con.commit()
    con.close()

def update_post(id, text):
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("""UPDATE posts SET sendText = ? WHERE id = ?""", (text, id))

    con.commit()
    con.close()

def update_post_flag(id, flag):
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("""UPDATE posts SET flag = ? WHERE id = ?""", (flag, id))

    con.commit()
    con.close()

def update_post_time(id, a):
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("""UPDATE posts SET year=?, month=?, day=?, hour=?, minute=? WHERE id = ?""",
                (int(a[4]), int(a[3]), int(a[2]), int(a[1]), int(a[0]), id))

    con.commit()
    con.close()

def delete_post():
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("""DELETE FROM posts WHERE flag = 1""")

    con.commit()
    con.close()