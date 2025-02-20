import speech_recognition as sr
from deep_translator import GoogleTranslator
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import os
from datetime import datetime

model_name = "Splintir/Nllb_dialecto"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
translator_pipe = pipeline("translation", model=model, tokenizer=tokenizer)

# Dictionary for supported languages
dictionary = {
    'eng': "eng_Latn",
    'ceb': "ceb_Latn",
    'hili': " "
}


# First install, initiate .dialecto app
def first_install():
    home_dir = os.path.expanduser("~") 
    app_dir = os.path.join(home_dir, ".dialecto_app")
    os.makedirs(app_dir, exist_ok=True)


# NLLB Dialecto Model
def nllb_model(text, direction):
    if direction == "ceb_to_eng":
        src_lang = dictionary["ceb"]
        tgt_lang = dictionary["eng"]
    else:  # eng_to_ceb
        src_lang = dictionary["eng"]
        tgt_lang = dictionary["ceb"]

    translated_text = translator_pipe(text, src_lang=src_lang, tgt_lang=tgt_lang, max_length=400)
    return translated_text[0]['translation_text']


# Deep Translator (counter checking)
def translate_deep(text):
    deeptrans = GoogleTranslator(source='auto', target='en')
    translated = deeptrans.translate(text)
    return translated


# Recording directory
def get_app_audio_directory():
    """Creates and returns the app's dedicated directory."""
    home_dir = os.path.expanduser("~") 
    app_dir = os.path.join(home_dir, ".dialecto_app/audio")

    os.makedirs(app_dir, exist_ok=True)  # Ensure directory exists
    return app_dir


# Return latest recorded file
def get_latest():
    homedir = os.path.expanduser("~")
    audiodir = os.path.join(homedir, ".dialecto_app/audio")

    files = [f for f in os.listdir(audiodir) if f.endswith(".wav")]
    if not files:
        print("No recordings found.")
        return None
    latest_recording = max(files, key=lambda f: os.path.getmtime(os.path.join(audiodir, f)))
    return os.path.join(audiodir, latest_recording)


# Text Translation
def transtext(text, direction):
    print(f"You said: {text}")
    print(f"(deeptranslate) translation: {translate_deep(text)}")
    print(f"(nllb_dialecto) translation: {nllb_model(text, direction)}")


# Recording Start
def record_voice(direction):
    """Records voice input and saves it in the app's directory."""
    save_folder = get_app_audio_directory()

    while True:
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening... Speak now!")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)

                print(f"You said: {text}")
                print(f"(deeptranslate) translation: {translate_deep(text)}")
                print(f"(nllb_dialecto) translation: {nllb_model(text, direction)}")
                break

        except sr.UnknownValueError:
            print("Couldn't recognize audio, please try again.")
        except sr.RequestError:
            print("Connection Problem")

    # Generate filename with timestamp
    print("=" * 90)
    filename = os.path.join(save_folder, f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")

    try:
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())

        print(f"Recording saved at: {filename}")
    except PermissionError:
        print(f"Permission denied: Unable to save file to {filename}. Try running as administrator.")


def main():
    first_install()
    while True:
        op = input("""

    Dialecto v1.0 Console Beta
        
        1. Translate audio [Cebuano -> English] 
        2. Translate text [Cebuano -> English]
        3. Translate audio [English -> Cebuano]
        4. Translate text [English -> Cebuano]
        5. Exit
        >> """)

        match op:
            case "1":
                record_voice("ceb_to_eng")
            case "2":
                text = input("Input text you want to translate: ")
                transtext(text, "ceb_to_eng")
            case "3":
                record_voice("eng_to_ceb")
            case "4":
                text = input("Input text you want to translate: ")
                transtext(text, "eng_to_ceb")
            case "5":
                print("Thank you for using our app.")
                break
            case _:
                print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
