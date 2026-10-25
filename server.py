
from datetime import datetime
from flask import Flask, jsonify, render_template

from data_generator import generate_data
from benchmark import benchmark_avl, benchmark_sqlite


app = Flask(__name__)

DATASET_SIZES = [1000, 5000, 10000, 50000, 100000]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/benchmark", methods=["POST"])
def run_benchmark_api():
    results = []

    try:
        for size in DATASET_SIZES:
            # Generate a fresh dataset for this test.
            data = generate_data(size)

            # Run both existing benchmark implementations.
            avl_time, avl_found = benchmark_avl(data, data[0])
            sqlite_time, sqlite_found = benchmark_sqlite(data, data[0])

            # Prepare results for the website.
            avl_found = bool(avl_found)
            sqlite_found = bool(sqlite_found)

            results.append({
                "dataset_size": size,
                "avl_time": round(float(avl_time), 3),
                "sqlite_time": round(float(sqlite_time), 3),
                "avl_found": avl_found,
                "sqlite_found": sqlite_found,
                "correctness": avl_found and sqlite_found
            })

        return jsonify({
            "success": True,
            "results": results,
            "completed_at": datetime.now().isoformat(
                timespec="seconds"
            )
        })

    except Exception:
        app.logger.exception("Benchmark execution failed")

        return jsonify({
            "success": False,
            "error": (
                "The benchmark failed. Check the server terminal "
                "for the detailed error."
            )
        }), 500


if __name__ == "__main__":
    print("=" * 48)
    print("       INDEXLAB BENCHMARK STUDIO")
    print("=" * 48)
    print("Starting local web server...")
    print("Open http://127.0.0.1:5000 in your browser.")
    print("Press CTRL+C in this terminal to stop.")
    print("=" * 48)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
