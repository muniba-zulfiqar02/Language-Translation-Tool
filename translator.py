# translator.py
# This file handles all translation logic

from deep_translator import GoogleTranslator

LANGUAGES = { 
    "ENGLISH" : "en" ,
    "French" : "fr" ,
    "Spanish" : "es" ,
    "German" : "de" ,
    "Hindi" :"hi" ,
    "Arabic" : "ar" ,
    "Chinese (Simplified)" : "zh-CN" ,
    "Japanese" : "ja" ,
    "Urdu" : "ur" ,
    "Portuguese" : "pt" ,
    "Russian" : "ru" ,
    "Italian" : "it" ,
    "Korean" : "ko" ,
    "Turkish" : "tr" ,
    "Dutch" : "nl" ,
    "Greek" : "el" ,
    "Swedish" : "sv" ,
    "Polish" : "pl" ,
    "Bengali" : "bn" ,
    "Punjabi" : "pa" ,
}
def translate (text, target_language):
    try:
        target_code = LANGUAGES[target_language]
        translated = GoogleTranslator(source='auto', target=target_code).translate (text)
        return translated
    except Exception as e:
        return f"Error: {str(e)}"
def get_language_list() :
    return list(LANGUAGES.keys())



