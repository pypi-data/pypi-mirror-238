import requests

def translate_text(text, source_lang='auto_awesome', target_lang='pt'):
    """
    Translates the given text from the source language to the target language using MyMemory API.
    
    :param text: The text to be translated.
    :type text: str
    
    :param source_lang: The language code of the source language. Default is 'en' for English.
    :type source_lang: str
    
    :param target_lang: The language code of the target language. Default is 'pt' for Portuguese.
    :type target_lang: str
    
    :return: The translated text.
    :rtype: str
    """
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair={source_lang}|{target_lang}"
    response = requests.get(url)
    translation = response.json()["responseData"]["translatedText"]
    return translation
