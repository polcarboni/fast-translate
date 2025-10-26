import os 
from pathlib import Path
import wordfreq

freq_dir = "freq_words"

lang_files = os.listdir()
lang_files = [f for f in lang_files if f.endswith(".txt")]

os.makedirs(freq_dir, exist_ok=True)

for lang_file in lang_files:
    
    lang_code = lang_file.split("_")[-1].split(".")[0]

    with open(lang_file, "r", encoding="utf-8") as src:
        words = src.readlines()
        words = [f"{w}: {wordfreq.word_frequency(w, 'en')}".replace("\n", "") for w in words]
        
        with open(f"{freq_dir}/wordsfreq_{lang_code}.txt", "w", encoding="utf-8") as dst:
            for w in words:
                dst.write(w + "\n")