
import time
import statistics
import matplotlib.pyplot as plt

from data_generator import generate_data
from avl_tree import AVLTree
from database import SQLiteDatabase


REPETITIONS = 5
SEARCH_COUNT = 100


def benchmark_avl(data, search_key=None):
    """Build an AVL tree, validate searches, and measure search latency."""

    tree = AVLTree()

    for value in data:
        tree.root = tree.insert(tree.root, value)

    # Test the same existing keys in every repetition.
    search_keys = data[:min(SEARCH_COUNT, len(data))]

    if not search_keys:
        return 0.0, False

    # Validate every search outside the timed section.
    all_found = all(
        tree.search(tree.root, key)
        for key in search_keys
    )

    timings = []

    for _ in range(REPETITIONS):
        start = time.perf_counter_ns()

        for key in search_keys:
            tree.search(tree.root, key)

        end = time.perf_counter_ns()

        average_us = (
            (end - start) / 1000 / len(search_keys)
        )

        timings.append(average_us)

    return statistics.median(timings), all_found


def benchmark_sqlite(data, search_key=None):
    """Build an indexed SQLite table, validate searches, and measure latency."""

    database = SQLiteDatabase()

    try:
        database.create_table()
        database.insert_data(data)

        search_keys = data[:min(SEARCH_COUNT, len(data))]

        if not search_keys:
            return 0.0, False

        # Validate every search outside the timed section.
        all_found = all(
            database.search(key)
            for key in search_keys
        )

        timings = []

        for _ in range(REPETITIONS):
            start = time.perf_counter_ns()

            for key in search_keys:
                database.search(key)

            end = time.perf_counter_ns()

            average_us = (
                (end - start) / 1000 / len(search_keys)
            )

            timings.append(average_us)

        return statistics.median(timings), all_found

    finally:
        database.close()


def run_benchmark():
    dataset_sizes = [1000, 5000, 10000, 50000, 100000]

    avl_results = []
    sqlite_results = []

    print("Relational Indexing vs Memory Trees")
    print("===================================")
    print("Scalability Benchmark")
    print(f"Searches per repetition: {SEARCH_COUNT}")
    print(f"Repetitions: {REPETITIONS}")
    print("Reported timing: median average search latency")
    print()

    all_tests_passed = True

    for size in dataset_sizes:
        print(f"Testing dataset size: {size}")

        data = generate_data(size)

        avl_time, avl_found = benchmark_avl(data)
        sqlite_time, sqlite_found = benchmark_sqlite(data)

        avl_results.append(avl_time)
        sqlite_results.append(sqlite_time)

        correct = avl_found and sqlite_found
        all_tests_passed = all_tests_passed and correct

        print(f"  AVL:    {avl_time:.3f} microseconds")
        print(f"  SQLite: {sqlite_time:.3f} microseconds")
        print(f"  All tested searches found: {correct}")
        print()

    print("===================================")
    print("Final Benchmark Results")
    print("===================================")

    for i, size in enumerate(dataset_sizes):
        print(
            f"{size:>7} records | "
            f"AVL: {avl_results[i]:>10.3f} µs | "
            f"SQLite: {sqlite_results[i]:>10.3f} µs"
        )

    print()
    print(f"Overall validation: {'PASS' if all_tests_passed else 'FAIL'}")

    plt.figure(figsize=(10, 6))
    plt.plot(dataset_sizes, avl_results, marker="o", label="AVL Tree")
    plt.plot(dataset_sizes, sqlite_results, marker="o", label="SQLite Indexed Search")

    plt.xlabel("Number of Records")
    plt.ylabel("Median Average Search Time (microseconds)")
    plt.title("Relational Indexing vs Memory Trees")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("performance_graph.png")

    print("Performance graph saved as performance_graph.png")

    plt.show()


if __name__ == "__main__":
    run_benchmark()
