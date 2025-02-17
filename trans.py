import speech_recognition as sr
from deep_translator import GoogleTranslator
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from datasets import load_dataset

pipe = pipeline("translation", model="facebook/nllb-200-distilled-600M")
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

def deep_trans(text):
    translator = GoogleTranslator(source='auto',target='en')
    return translator.translate(text)

def nllb_model(text):
    translator=pipeline('translation', model=model, tokenizer=tokenizer, src_lang='ceb_Latn', tgt_lang='eng_Latn', max_length = 400)
    #print(type(translator))
    translated_text = translator(text)
    return translated_text[0]['translation_text']

dataset = load_dataset('')

def getinput():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for command...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        bydeeptrans = deep_trans(text)
        print("(deep_translator)Translated: " + bydeeptrans)
        print("\n===================================================================\n")
        bynllb = nllb_model(text)
        print("(nllb_model)Translated: " + bynllb)
    except sr.UnknownValueError:
        print("couldnt recognize")
    except sr.RequestError:
        print("request failed(please use microphone)")

if __name__ == "__main__":
    getinput()

