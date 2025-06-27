# sele_sira_bot/bot/utils/formatter.py
from translations import en, am

def get_translation(lang: str = 'en'):
    if lang == 'am':
        return am.STRINGS
    return en.STRINGS
