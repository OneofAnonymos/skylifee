import sqlite3

DB_NAME = "skylife.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    c = conn.cursor()

    # جدول پروفایل کاربران
    c.execute('''CREATE TABLE IF NOT EXISTS profiles (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        money INTEGER DEFAULT 100,
        level INTEGER DEFAULT 1,
        xp INTEGER DEFAULT 0,
        energy INTEGER DEFAULT 100,
        happiness INTEGER DEFAULT 100,
        sleep INTEGER DEFAULT 100,
        hunger INTEGER DEFAULT 100,
        city TEXT DEFAULT 'تهران',
        job TEXT DEFAULT NULL,
        married_to INTEGER DEFAULT NULL
    )''')

    # جدول مهارت‌ها
    c.execute('''CREATE TABLE IF NOT EXISTS skills (
        user_id INTEGER,
        skill_name TEXT,
        level INTEGER DEFAULT 1,
        PRIMARY KEY(user_id, skill_name)
    )''')

    # آیتم‌های کاربر
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
        user_id INTEGER,
        item TEXT,
        amount INTEGER,
        PRIMARY KEY(user_id, item)
    )''')

    # حیوان خانگی
    c.execute('''CREATE TABLE IF NOT EXISTS pets (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        happiness INTEGER DEFAULT 100,
        hunger INTEGER DEFAULT 100
    )''')

    # ازدواج
    c.execute('''CREATE TABLE IF NOT EXISTS relationships (
        user1 INTEGER,
        user2 INTEGER,
        status TEXT,
        PRIMARY KEY(user1, user2)
    )''')

    conn.commit()
    conn.close()