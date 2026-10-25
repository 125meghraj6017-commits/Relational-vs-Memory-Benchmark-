import matplotlib.pyplot as plt


dataset_sizes = [1000, 5000, 10000, 50000, 100000]

avl_times = [
    1.077,
    0.995,
    0.968,
    1.054,
    1.043
]

sqlite_times = [
    173.172,
    178.272,
    92.403,
    175.865,
    172.808
]


plt.figure(figsize=(10, 6))

plt.plot(
    dataset_sizes,
    avl_times,
    marker="o",
    label="AVL Tree"
)

plt.plot(
    dataset_sizes,
    sqlite_times,
    marker="o",
    label="SQLite B-Tree"
)

plt.xlabel("Number of Records")
plt.ylabel("Average Search Time (microseconds)")

plt.title("Relational Indexing vs Memory Trees")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.show()