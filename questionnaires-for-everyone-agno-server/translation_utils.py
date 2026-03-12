import os
import threading
from functools import lru_cache

# Set Argos Translate to use a local directory for data and packages
ARGOS_DIR = os.path.abspath(os.path.join(os.getcwd(), '.argos-translate'))
os.makedirs(ARGOS_DIR, exist_ok=True)

# Important: set these BEFORE any argostranslate import
os.environ['XDG_DATA_HOME'] = os.path.join(ARGOS_DIR, 'data')
os.environ['XDG_CONFIG_HOME'] = os.path.join(ARGOS_DIR, 'config')
os.environ['XDG_CACHE_HOME'] = os.path.join(ARGOS_DIR, 'cache')

# Ensure subdirectories exist
os.makedirs(os.environ['XDG_DATA_HOME'], exist_ok=True)
os.makedirs(os.environ['XDG_CONFIG_HOME'], exist_ok=True)
os.makedirs(os.environ['XDG_CACHE_HOME'], exist_ok=True)

import argostranslate.package
import argostranslate.translate

# Global cache for translation objects to avoid repeated disk lookups
_TRANSLATORS = {}
_LOCK = threading.Lock()

def get_translator(from_code, to_code):
    """Retrieves or creates a translator object for the given language pair."""
    pair_id = f"{from_code}_{to_code}"
    
    with _LOCK:
        if pair_id in _TRANSLATORS:
            return _TRANSLATORS[pair_id]
        
        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = next(filter(lambda x: x.code == from_code, installed_languages), None)
        to_lang = next(filter(lambda x: x.code == to_code, installed_languages), None)
        
        if from_lang and to_lang:
            translator = from_lang.get_translation(to_lang)
            if translator:
                _TRANSLATORS[pair_id] = translator
                return translator
    return None

def ensure_language_installed(from_code, to_code):
    """Ensures that the specific language pair package is installed."""
    if get_translator(from_code, to_code):
        return True

    try:
        print(f"Installing translation model for {from_code} -> {to_code}...")
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        package_to_install = next(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
            ), None
        )
        if package_to_install:
            print(f"Downloading package: {package_to_install}")
            argostranslate.package.install_from_path(package_to_install.download())
            # Reset cache to pick up new language
            with _LOCK:
                _TRANSLATORS.clear()
            return True
        else:
            print(f"No package found for {from_code} -> {to_code}")
            return False
    except Exception as e:
        print(f"Error ensuring language package: {e}")
        return False

def warm_up(from_lang='en', to_lang='pt'):
    """Pre-loads the translator into memory to avoid delay on first request."""
    print(f"Warming up Argos Translate for {from_lang} -> {to_lang}...")
    from_code = from_lang.lower()[:2]
    to_code = to_lang.lower()[:2]
    if ensure_language_installed(from_code, to_code):
        get_translator(from_code, to_code)
        print("Warm-up complete.")

def translate_statements(item_list, from_lang, to_lang):
    from_code = from_lang.lower()[:2]
    to_code = to_lang.lower()[:2]
    
    ensure_language_installed(from_code, to_code)
    translator = get_translator(from_code, to_code)
    
    if not translator:
        return item_list

    return [translator.translate(item) for item in item_list]

def translate_statement_pairs(item_list, from_lang, to_lang):
    from_code = from_lang.lower()[:2]
    to_code = to_lang.lower()[:2]
    
    ensure_language_installed(from_code, to_code)
    translator = get_translator(from_code, to_code)
    
    if not translator:
        return item_list

    translated_pairs = []
    for pair in item_list:
        translated_pairs.append([translator.translate(item) for item in pair])
    
    return translated_pairs

def translate(item, from_lang, to_lang):
    """Legacy single item translate function."""
    from_code = from_lang.lower()[:2]
    to_code = to_lang.lower()[:2]
    
    translator = get_translator(from_code, to_code)
    if translator:
        return translator.translate(item)
    return item