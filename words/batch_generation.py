import asyncio
import httpx
from tqdm import tqdm

LANGUAGE_CODES = [
    #"en",  # English
    #"h-CN",  # Chinese (Simplified)
    #"es",  # Spanish
    #"ar",  # Arabic
    #"hi",  # Hindi
    #"fr",  # French
    # "bn",  # Bengali
    #"ru",  # Russian
    #"pt",  # Portuguese
    # "id",  # Indonesian
    # "ur",  # Urdu
    #"de",  # German
    # "ja",  # Japanese
    # "sw",  # Swahili
    # "mr",  # Marathi
    # "ta",  # Tamil
    # "te",  # Telugu
    # "vi",  # Vietnamese
    # "ko",  # Korean
    #"it",  # Italian
    # "th",  # Thai
    # "tr",  # Turkish
    # "gu",  # Gujarati
    # "kn",  # Kannada
    # "pa",  # Punjabi
    # "ml",  # Malayalam
    # "or",  # Odia
    #"cs",  # Czech
    #"pl",  # Polish
    #"ro",  # Romanian
    #"nl",  # Dutch
    #"el",  # Greek
    # "hu",  # Hungarian
    #"sv",  # Swedish
    #"fi",  # Finnish
    # "he",  # Hebrew
    "da",  # Danish
    "no",  # Norwegian
    #"bg",  # Bulgarian
    #"uk",  # Ukrainian
    #"sr",  # Serbian
    #"sk",  # Slovak
    # "sl",  # Slovenian
    # "hr",  # Croatian
    # "ka",  # Georgian
    "hy",  # Armenian
    # "az",  # Azerbaijani
    # "bs",  # Bosnian
    # "cy",  # Welsh
    # "af",  # Afrikaans
    "sq",  # Albanian
    # "eu",  # Basque
    # "ht",  # Haitian Creole
    # "gl",  # Galician
    # "jv",  # Javanese
    # "yi",  # Yiddish
    # "tl",  # Filipino
    # "is",  # Icelandic
    # "mt",  # Maltese
]


async def translate_word(client, word, src="en", dest="fr"):
    '''Translates a word using the google tranlate api.'''
    
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": src,
        "tl": dest,
        "dt": "t",
        "q": word
    }
    
    try:
        r = await client.get(url, params=params, timeout=10.0)
        r.raise_for_status()
        return r.json()[0][0][0]
    
    except Exception:
        return f"%ERR_{word}"


async def main():
    
    with open("words_en.txt") as f:
        words = [w.strip() for w in f.readlines()]
    
    for dest_lang in LANGUAGE_CODES:

        with open(f"words_{dest_lang}.txt", "w", encoding="utf-8") as f:
            pass

        results = []
        semaphore = asyncio.Semaphore(50)  # Limit concurrency

        async with httpx.AsyncClient() as client:
            
            async def safe_translate(word, dest_lang):
                async with semaphore:
                    return await translate_word(client, word,  src="en", dest=dest_lang)

            for i in tqdm(range(0, len(words), 500)):
                batch = words[i:i+500]
                translations = await asyncio.gather(*[safe_translate(w, dest_lang) for w in batch])
                results.extend(translations)

                with open(f"words_{dest_lang}.txt", "a", encoding="utf-8") as f:
                    f.write("\n".join(translations) + "\n")

    print("Done!")


asyncio.run(main())
