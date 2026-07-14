import sqlite3
from loader import Loader

DB_NAME = "db/nifty100.db"


def main():
    print("Starting ETL load...")

    loader = Loader()
    loader.run()

    print("ETL complete ✔")


if __name__ == "__main__":
    main()