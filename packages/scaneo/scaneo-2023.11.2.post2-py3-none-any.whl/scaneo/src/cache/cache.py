import sqlite3
import os


def get_cache_dir():
    home_dir = os.path.expanduser("~")
    cache_dir = os.path.join(home_dir, ".cache/scaneo/")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    return cache_dir


def create_database():
    conn = sqlite3.connect(get_cache_dir() + "database.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT)"
    )
    conn.commit()
    conn.close()


def persist_dict_in_db(dict):
    conn = sqlite3.connect(get_cache_dir() + "database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cache")
    cursor.executemany(
        "INSERT INTO cache (key, value) VALUES (?, ?)",
        [(img["name"], str(",".join(map(str, img["bbox"])))) for img in dict],
    )
    conn.commit()
    conn.close()


def get_dict_from_db():
    conn = sqlite3.connect(get_cache_dir() + "database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM cache")
    rows = cursor.fetchall()
    return [
        {"name": row[0], "bbox": list(map(float, row[1].split(",")))} for row in rows
    ]
