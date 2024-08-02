import json
import os

class Trans:
    def __init__(self):
        self.language = 'vi'
        self.load_path = 'src/locales/'
        self.translations = self.load_translations()

    def load_translations(self):
        locale_path = os.path.join(self.load_path, f'{self.language}.json')
        absolute_path = os.path.abspath(locale_path)
        if os.path.exists(absolute_path):
            with open(absolute_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            print(f"Translation file {absolute_path} does not exist.")
            return {}

    def _(self, text):
        return self.get_translation(text)
    
    def objectT(self, text):
        return self.firstLetterUppercase(self.get_translation(f"object.{text}"))
    
    def MessageT(self, text):
        return self.get_translation(f"message.{text}")
    
    def firstLetterUppercase(self, text: str):
        return text.capitalize()
    
    def message(self, text: str):
        arr = text.split('.')
        obj = self.firstLetterUppercase(self.get_translation(f"object.{arr[1]}"))
        mes = self.MessageT(arr[0])
        return obj + " " + mes
    
    def get_translation(self, text):
        keys = text.split('.')
        translation = self.translations
        for key in keys:
            translation = translation.get(key)
            if translation is None:
                return f"Missing translation for {self.language}.{text}"
        return translation