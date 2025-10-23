from googletrans import Translator
import time
import asyncio
from tqdm import tqdm
import httpx

translator = Translator()

with open("words_en.txt", "r") as f:
    words = [word.strip() for word in f.readlines()]
    
TARGET_LANGS = ["de"]
BATCH_SIZE = 64
RETRY_DELAY = 1.0
MAX_RETRIES = 3


async def translate_with_retry(word, src, dest, max_retries, retry_delay):
    for attempt in range(max_retries):
        try:
            translated = await translator.translate(word, src=src, dest=dest)
            if translated and translated.text:
                return translated.text
            else:
                print(f"Translation error: {word}")
                return f"%ERR_{word}"
        except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError) as e:
            if attempt < max_retries - 1: 
                await asyncio.sleep(retry_delay)
            else:
                print(f"Translation error after {max_retries} retries: {word}")
                return f"%ERR_{word}"
        except Exception as e:
            print(f"Unexpected error: {word}")
            return f"%ERR_{word}"
        
        
async def main():
    for target_lang in TARGET_LANGS:
        print(f"Started translation to {target_lang}.")

        for i in tqdm(range(0, len(words), BATCH_SIZE), desc=f"Translating vocab to {target_lang}"):
            
            batch = words[i:i+BATCH_SIZE]
            translated_words = []
            print("Translating batch number: ", i)
            print(batch)
            
            # Translation loop:
            # Connection or timeout errors: retry. Error in translation or unknown: %ERR_originalword 
            
            for word in batch:
                translated_word = await translate_with_retry(word,
                                                                src="en",
                                                                dest=target_lang,
                                                                max_retries=MAX_RETRIES,
                                                                retry_delay=RETRY_DELAY)
                translated_words.append(translated_word)
                    
            with open(f"words_{target_lang}.txt", "a") as f:
                for translated_word in translated_words:
                    f.write(str(translated_word)+"\n")

            await asyncio.sleep(0.5)

asyncio.run(main())