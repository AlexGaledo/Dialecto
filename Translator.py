
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import speech_recognition as sr
from googletrans import Translator
from deep_translator import GoogleTranslator
import asyncio  # Import asyncio to handle async functions


model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

async def nllb(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    output = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id["eng_Latn"])
    translated_text = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    return translated_text

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

def nllbdistilled():
    print("------------------")
    translate_text3 = asyncio.run(nllb(text)) # deeptrans
    print("(nllb-distilled-600M)Translated Text:", translate_text3)


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
    nllbdistilled()

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))



