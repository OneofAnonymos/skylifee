from db import connect

def get_user_profile(user_id):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT money, xp, level, energy, happiness, hunger, sleep FROM profiles WHERE user_id = ?", (user_id,))
    profile = c.fetchone()
    conn.close()
    return profile

def update_profile(user_id, field, amount):
    conn = connect()
    c = conn.cursor()
    c.execute(f"UPDATE profiles SET {field} = {field} + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def format_number(n):
    return f"{n:,}"

def level_up_check(user_id):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT xp, level FROM profiles WHERE user_id = ?", (user_id,))
    xp, level = c.fetchone()
    next_level_xp = level * 100 + 100

    if xp >= next_level_xp:
        c.execute("UPDATE profiles SET level = level + 1, xp = xp - ? WHERE user_id = ?", (next_level_xp, user_id))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False