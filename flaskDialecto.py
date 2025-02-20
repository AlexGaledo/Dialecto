from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import os
import speech_recognition as sr

app = Flask(__name__)
model_name = "Splintir/Nllb_dialecto"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
translator_pipe = pipeline("translation", model=model, tokenizer=tokenizer)

# Dictionary for supported languages
dictionary = {
    'eng': "eng_Latn",
    'ceb': "ceb_Latn"
}

def get_audio_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Could not request results"

@app.route("/", methods=["GET", "POST"])
def home():
    translation = ""
    input_text = ""
    if request.method == "POST":
        input_text = request.form.get("text", "")
        direction = request.form.get("direction", "")
        
        if direction == "ceb_to_eng":
            src_lang = dictionary["ceb"]
            tgt_lang = dictionary["eng"]
        elif direction == "eng_to_ceb":
            src_lang = dictionary["eng"]
            tgt_lang = dictionary["ceb"]
        
        translated_text = translator_pipe(input_text, src_lang=src_lang, tgt_lang=tgt_lang, max_length=400)
        translation = translated_text[0]['translation_text']
    
    return render_template("index.html", translation=translation, input_text=input_text)

@app.route("/microphone", methods=["POST"])
def microphone():
    text = get_audio_input()
    return jsonify({"text": text})

if __name__ == "__main__":
    app.run()
