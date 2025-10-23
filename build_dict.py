import time
start_time = time.time()
with open("words.txt", "r") as f:
    words = f.readlines()
end_time = time.time()
print(f"Word reading time: {end_time-start_time:.6f}")
