from deep_translator import GoogleTranslator
from langdetect import detect 

text = "Oww InanaKadali com barrata saratakam Jnanakagdan masoiya esakam guranchifrari chaoiyunaka sinsi sanda0 gouraula sinchasdam prardi 1kkam nichi; Gauriya Mustashudu Simpolu Boraya Esakam Orakam' This Baragiudu Rama vyakih60riprayas yamanga respect 56665 56665na5 Basu Geikeni regiyuka Kagnama to Kaginagaurasah ivvipardasa'"

print("Langdetect says:", detect(text))

try:
    print("GoogleTranslator translated:", GoogleTranslator(source='auto', target='en').translate(text))
except Exception as e:
    print(e)
