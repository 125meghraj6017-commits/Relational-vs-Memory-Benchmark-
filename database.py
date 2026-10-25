import sqlite3


class SQLiteDatabase:

    def __init__(self, db_name="benchmark.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS records")

        self.cursor.execute("""
            CREATE TABLE records (
                id INTEGER PRIMARY KEY,
                value INTEGER
            )
        """)

        self.cursor.execute("""
            CREATE INDEX idx_value
            ON records(value)
        """)

        self.connection.commit()

    def insert_data(self, data):
        self.cursor.executemany(
            "INSERT INTO records (value) VALUES (?)",
            [(value,) for value in data]
        )

        self.connection.commit()

    def search(self, value):
        self.cursor.execute(
            "SELECT value FROM records WHERE value = ?",
            (value,)
        )

        return self.cursor.fetchone() is not None

    def close(self):
        self.connection.close()


if __name__ == "__main__":

    from data_generator import generate_data

    data = generate_data(1000)

    database = SQLiteDatabase()
    database.create_table()
    database.insert_data(data)

    search_key = data[0]

    print("SQLite Database Module")
    print("----------------------")
    print("Records inserted:", len(data))
    print("Search key:", search_key)
    print("Search result:", database.search(search_key))

    database.close()

    print("SQLite module working successfully.")