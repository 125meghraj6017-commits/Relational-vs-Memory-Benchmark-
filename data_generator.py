import random
def generate_data(size):
    """Generate a list of unique integer records."""
    return random.sample(range(1, size * 10 +1), size)

if __name__ == "__main__":
    data = generate_data(1000)    
    print("Data Input Module")
    print("-----------------")
    print(f"Records generated: {len(data)}")
    print(f"First 10 records:{data[:10]}")
