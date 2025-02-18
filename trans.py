import speech_recognition as sr
from deep_translator import GoogleTranslator
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import torch

device = torch.device("cuda"if torch.cuda.is_available()else "cpu")
print(f"Using device: {device}")

pipe = pipeline("translation", model="Splintir/Nllb_dialecto/model/fine_tuned_nllb")
tokenizer = AutoTokenizer.from_pretrained("Splintir/Nllb_dialecto/model/fine_tuned_nllb")
model = AutoModelForSeq2SeqLM.from_pretrained("Splintir/Nllb_dialecto/model/fine_tuned_nllb")

def deep_trans(text):
    translator = GoogleTranslator(source='auto',target='en')
    return translator.translate(text)


def nllb_model(text):
    translator=pipeline('translation', model=model, tokenizer=tokenizer, src_lang='ceb_Latn', tgt_lang='eng_Latn', max_length = 400)
    translated_text = translator(text)
    return translated_text[0]['translation_text']

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

