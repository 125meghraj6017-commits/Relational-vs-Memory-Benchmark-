
import os
import tempfile

from avl_tree import AVLTree
from database import SQLiteDatabase


def test_avl_tree():
    tree = AVLTree()
    values = [10, 20, 30, 40, 50, 25]

    for value in values:
        tree.root = tree.insert(tree.root, value)

    # Every inserted value should be found.
    for value in values:
        assert tree.search(tree.root, value) is True, (
            f"AVL failed to find {value}"
        )

    # Missing values should not be found.
    missing_values = [-100, 0, 15, 35, 1000]

    for value in missing_values:
        assert tree.search(tree.root, value) is False, (
            f"AVL incorrectly found missing value {value}"
        )

    print("PASS: AVL tree finds existing values")
    print("PASS: AVL tree rejects missing values")


def test_sqlite():
    values = [10, 20, 30, 40, 50, 25]

    # Use a temporary database so the project database is untouched.
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test.db")
        database = SQLiteDatabase(db_path)

        try:
            database.create_table()
            database.insert_data(values)

            for value in values:
                assert database.search(value) is True, (
                    f"SQLite failed to find {value}"
                )

            missing_values = [-100, 0, 15, 35, 1000]

            for value in missing_values:
                assert database.search(value) is False, (
                    f"SQLite incorrectly found missing value {value}"
                )

            # Confirm the database index exists.
            database.cursor.execute(
                "PRAGMA index_list(records)"
            )
            indexes = database.cursor.fetchall()

            assert any(
                index[1] == "idx_value" for index in indexes
            ), "SQLite index idx_value is missing"

        finally:
            database.close()

    print("PASS: SQLite finds existing values")
    print("PASS: SQLite rejects missing values")
    print("PASS: SQLite index exists")


if __name__ == "__main__":
    print("=" * 42)
    print("PROJECT CORRECTNESS TESTS")
    print("=" * 42)

    test_avl_tree()
    test_sqlite()

    print("=" * 42)
    print("ALL TESTS PASSED!")
    print("=" * 42)
