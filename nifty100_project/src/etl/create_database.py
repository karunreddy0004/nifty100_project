import sqlite3
from pathlib import Path


def create_db():
    db_path = Path("db/nifty100.db")
    schema_path = Path("db/schema.sql")

    conn = sqlite3.connect(db_path)

    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()

    print("Database created successfully ✔")


if __name__ == "__main__":
    create_db()