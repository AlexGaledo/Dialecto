from flask import Flask,request, jsonify
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import os
import speech_recognition as sr
import requests
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

#Mistral AI
load_dotenv("deepkey.env")
MISTRAL_KEY = os.getenv("MISTRAL_KEY")

model_name = "Splintir/Nllb_dialecto"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
translator_pipe = pipeline("translation", model=model, tokenizer=tokenizer)


# Dictionary for supported languages
dictionary = {
    'eng': "eng_Latn",
    'ceb': "ceb_Latn"
}

def nllb_model(text, direction):
    if direction == "ceb_to_eng":
        src_lang = dictionary["ceb"]
        tgt_lang = dictionary["eng"]
    else:  # eng_to_ceb
        src_lang = dictionary["eng"]
        tgt_lang = dictionary["ceb"]

    translated_text = translator_pipe(text, src_lang=src_lang, tgt_lang=tgt_lang, max_length=400)
    return translated_text[0]['translation_text']


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
    

@app.route("/microphone", methods=["POST"])
def microphone():
    text = get_audio_input()
    return jsonify({"text": text})


@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_input = request.get_json().get("text", "")  # Ensure we are getting JSON data
    direction = "ceb_to_eng"  # Always translate from Cebuano to English first

    print(f"User Input: {user_input}")  # Debugging

    # Step 1: Translate Cebuano to English
    try:
        translated_text = nllb_model(user_input, direction)
        print(f"Translated Text: {translated_text}")  # Debugging
    except Exception as e:
        print(f"Translation Error: {e}")
        return jsonify({"error": "Translation failed"}), 500

    # Step 2: Send translated English text to DeepSeek Chat
    try:
        chatbot_response = get_chatbot_response(translated_text)
        print(f"Chatbot Response: {chatbot_response}")  # Debugging
    except Exception as e:
        print(f"Chatbot API Error: {e}")
        return jsonify({"error": "Chatbot request failed"}), 500

    return jsonify({
        "translated_text": translated_text,  
        "chatbot_response": chatbot_response  
    })





def get_chatbot_response(text):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_KEY}", "Content-Type": "application/json"}

    data = {
        "model": "mistral-tiny",  # Try "mistral-small" if needed
        "messages": [{"role": "user", "content": text}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        # Debugging: Print the entire response
        response_json = response.json()
        print("Mistral API Response:", response_json)

        # Extract chatbot response
        return response_json.get("choices", [{}])[0].get("message", {}).get("content", "No response")
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"





if __name__ == "__main__":
    app.run()
