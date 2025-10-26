import time
import os
from pathlib import Path

start_time = time.time()

lang_dir = os.path.join(Path(__file__).parent, "words")

for file in os.listdir(lang_dir):
    
    if file.endswith('.txt'):
        langcode = file.split("_")[-1].split(".")[0]
        print(file, langcode)

        with open(f"{lang_dir}/{file}", "r") as f:
            word_langcode = []
            line = f.readlines()
            

end_time = time.time()
print(f"Word reading time: {end_time-start_time}")
