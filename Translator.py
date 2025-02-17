
import speech_recognition as sr
from googletrans import Translator
from deep_translator import GoogleTranslator
import asyncio  # Import asyncio to handle async functions

async def translate_text(text):
    translator = Translator()
    translated = await translator.translate(text, dest="en")
    return translated.text

async def deep_trans(text):
    translator = GoogleTranslator(source ='auto', target='en')
    return translator.translate(text)

def googletrans():
    print("------------------")
    translated_text = asyncio.run(translate_text(text)) # google trans
    print("(googletrans)Translated Text:", translated_text)

def deeptrans():
    print("------------------")
    translate_text2 = asyncio.run(deep_trans(text)) # deeptrans
    print("(deep-translator)Translated Text:", translate_text2)

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Adjusting for ambient noise... Please wait.")
    recognizer.adjust_for_ambient_noise(source)
    print("Listening for command...")
    audio = recognizer.listen(source)

try:
    print("Recognizing...")
    text = recognizer.recognize_google(audio)
    print("You said:", text)
    googletrans()
    deeptrans()

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))


def googletrans():
    print("------------------")
    translated_text = asyncio.run(translate_text(text))  # googletrans
    print("(googletrans)Translated Text:", translated_text)

def deeptrans():
    print("------------------")
    translate_text2 = asyncio.run(deep_trans(text)) # deeptrans
    print("(deep-translator)Translated Text:", translate_text2)


