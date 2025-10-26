#!/usr/bin/env python3
import argparse
import sys
import readline
import os
from pathlib import Path

def main():

    os.system('cls' if os.name == 'nt' else 'clear')

    parser = argparse.ArgumentParser(
        prog="ft",
        description="Fast cli translation tool"
    )

    parser.add_argument("source_lang")
    parser.add_argument("target_lang")

    args = parser.parse_args()

    # Application header
    print("--"*31)
    print(" "*16 +f"Fast-Translate :     ({args.source_lang} → {args.target_lang})")
    print("--"*31+"\n")
    

    lang_dir = os.path.join(Path(__file__).parent, "words")
    
    source_dict_path = Path(lang_dir + f"/words_{args.source_lang}.txt")
    target_dict_path = Path(lang_dir + f"/words_{args.target_lang}.txt")

    dictionary = {}

    with open(source_dict_path, "r", encoding="utf-8") as src:
        with open(target_dict_path, "r", encoding="utf-8") as dst:
            for s, t in zip(src, dst):
                 dictionary[s.strip().lower()] = t.strip().lower()

    inputs = []
    
    while True:
        word = input("> ").strip()

        try:
            result = dictionary.get(word.lower())
            if result is not None:
                print(f"{word}: {result}")
            else:
                print("Word not found.")

        except ValueError as e:
            print("Word not found.\n")


        inputs.append(word)
        '''
        for _ in range(2):
            sys.stdout.write("\033[F\033[K")
        sys.stdout.flush()
        '''


if __name__ == "__main__":
    main()