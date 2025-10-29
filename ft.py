#!/usr/bin/env python3
import argparse
import sys
import readline
import os
from pathlib import Path

def main():

    #TODO: add execution and terminal cleaning for Windows anc macOS
    os.system('cls' if os.name == 'nt' else 'clear') #Clear the terminal on linux

    parser = argparse.ArgumentParser(
        prog="ft",
        description="Fast cli translation tool"
    )

    parser.add_argument("--source_lang", "-s", type=str, default="de", help="Source langauge")
    parser.add_argument("--target_lang", "-t",  type=str, default="en", help="Destination language")
    parser.add_argument("--disambiguation_len", type=int, default=1, help="Max showed translations")
    parser.add_argument("--search", type=bool, default=False, help="Search translation if word is not present. Update the source files.")
    parser.add_argument("--phonetic", type=bool, default=False, help="Show phonetic alphabet version of the word.")
    args = parser.parse_args()

    # ------------------------- Commands list --------------------------
    #TODO: structure commands with {name, description, implementation}.
    
    commands = {
        "--help": "Show the command list",
        "--clear": "Clears the translator terminal",
        "--default_src": "Sets default source language",
        "--default_dst": "Sets default target language",
    }

    #------------------------- Print header --------------------------
    #TODO: Refactor, extract
    
    print("--"*31)
    print(" "*16 +f"Fast-Translate :     ({args.source_lang} → {args.target_lang})")
    print("--"*31+"\n")
    
    
    #------------------------- Load dictionary --------------------------
    #TODO: refactor, extract
    
    lang_dir = os.path.join(Path(__file__).parent, "words/freq_words")
    
    source_dict_path = Path(lang_dir + f"/wordsfreq_{args.source_lang}.txt")
    target_dict_path = Path(lang_dir + f"/wordsfreq_{args.target_lang}.txt")

    dictionary = {}

    with open(source_dict_path, "r", encoding="utf-8") as src:
        with open(target_dict_path, "r", encoding="utf-8") as dst:
            for s, t in zip(src, dst):
                source_word = s.split(":")[0].strip().lower()
                target_word = t.split(":")[0].strip().lower()
                target_score = float(t.split(":")[1])
                
                #Disambiguation: select the most used word as the result
                if source_word not in dictionary:
                    dictionary[source_word] = {"word" : target_word, "score" : target_score}
                else:
                    max_score = dictionary[source_word].get("score")
                    if target_score > float(max_score):
                        dictionary[source_word] = {"word" : target_word, "score" : target_score}
                        
    for word in dictionary:
        dictionary[word] = dictionary[word].get("word")
        
    
    # -------------------------------------------------------------------
    #                           Terminal input
    # -------------------------------------------------------------------
    
    while True:
        word = input("> ").strip()

        # -------------------------- Commands --------------------------
        if word.startswith("--"):
            if word in commands.keys():
                print(commands[word])
            else:
                print("Command is not available, available commands:\n")
                for name, desc in commands.items():
                    print(f"  {name:<15} {desc}")
            continue
        
        # ------------------------- Translation --------------------------
        try:
            result = dictionary.get(word.lower())
            if result is not None:
                print(f"{word}: {result}\n")
            else:
                print("Word not found.\n")

        except ValueError as e:
            print("Word not found.\n")

        #print("\n")
    
        # ------------------------- Terminal clean --------------------------
        #TODO: implement logic based on length of last command (can be multiple lines)
        '''
        for _ in range(2):
            sys.stdout.write("\033[F\033[K")
        sys.stdout.flush()
        '''


if __name__ == "__main__":
    main()