import sqlite3

def connect():
    return sqlite3.connect("skylife.db")

def init_db():
    conn = connect()
    c = conn.cursor()

    # جدول پروفایل کاربر
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            money INTEGER DEFAULT 1000,
            level INTEGER DEFAULT 1,
            energy INTEGER DEFAULT 100,
            happiness INTEGER DEFAULT 100,
            hunger INTEGER DEFAULT 0,
            sleep INTEGER DEFAULT 100,
            xp INTEGER DEFAULT 0,
            location TEXT DEFAULT 'تهران'
        )
    ''')

    # جدول شغل
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            user_id INTEGER PRIMARY KEY,
            job TEXT,
            salary INTEGER,
            level INTEGER
        )
    ''')

    # جدول مهارت‌ها
    c.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            user_id INTEGER,
            skill TEXT,
            level INTEGER,
            PRIMARY KEY (user_id, skill)
        )
    ''')

    # جدول آیتم‌ها
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            user_id INTEGER,
            item TEXT,
            amount INTEGER,
            PRIMARY KEY (user_id, item)
        )
    ''')

    # جدول حیوان خانگی
    c.execute('''
        CREATE TABLE IF NOT EXISTS pets (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            happiness INTEGER,
            level INTEGER
        )
    ''')

    # جدول ازدواج
    c.execute('''
        CREATE TABLE IF NOT EXISTS relationships (
            user_id INTEGER PRIMARY KEY,
            partner_id INTEGER
        )
    ''')

    # جدول مبارزه و XP مبارزه
    c.execute('''
        CREATE TABLE IF NOT EXISTS battle_stats (
            user_id INTEGER PRIMARY KEY,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()
