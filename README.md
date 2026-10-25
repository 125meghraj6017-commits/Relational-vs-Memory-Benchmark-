# Relational Indexing vs Memory Trees: A Benchmarking Study

## Overview

This project compares search performance between an in-memory AVL Tree and an SQLite database using an indexed column. It measures search latency across multiple dataset sizes and presents the results through a local web dashboard.

## Features

- AVL Tree implementation with self-balancing rotations
- SQLite database with an index on the `value` column
- Random dataset generation
- Repeated search benchmarks using high-resolution timing
- Interactive dashboard with chart scale controls
- Detailed benchmark results and CSV export
- Correctness tests for searches and database indexing

## Technologies

- Python
- Flask
- SQLite
- Matplotlib
- HTML, CSS and JavaScript

## Requirements

Python and the packages listed in `requirements.txt` are required.

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Application

From the project directory, run:

```bash
python server.py
```

Open this address in your browser:

http://127.0.0.1:5000

## Run Correctness Tests

```bash
python test_benchmark.py
```

## Benchmark Methodology

The benchmark compares search operations across datasets of 1,000, 5,000, 10,000, 50,000 and 100,000 records. Search timings are repeated, and the median of the average search latencies is reported.

Dataset generation and data-structure/database setup are excluded from the timed search section. Results depend on the machine, software environment and implementation.

## Limitations

- Results represent this particular implementation and test environment.
- The AVL Tree is an in-memory data structure, while SQLite provides database functionality and persistence.
- Search latency alone does not capture all differences between the two approaches.
- Benchmark results may vary between runs and computers.

## Project Purpose

This project is an educational benchmarking study intended to compare search behaviour and discuss the trade-offs between in-memory tree structures and indexed relational databases.