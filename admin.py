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
                year INT,
                month INT,
                day INT,
                hour INT,
                minute INT,
                flag INT
            )""")

def select_user(id):
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("SELECT * FROM users WHERE id=?", (int(id),))
    result = cur.fetchone()

    con.close()

    return result

def select_post():
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("SELECT * FROM posts")
    resultpost = cur.fetchone()

    con.close()

    return resultpost


def create_user(id):
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("INSERT INTO users values (?, 0)", (int(id),))

    con.commit()
    con.close()

def update_user_flag(id, flag):
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()

    cur.execute("""UPDATE users SET flag = ? WHERE id = ?""", (flag, id))

    con.commit()
    con.close()