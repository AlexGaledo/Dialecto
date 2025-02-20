import speech_recognition as sr
from deep_translator import GoogleTranslator
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import os
from datetime import datetime

model_name = "Splintir/Nllb_dialecto"
pipe = pipeline("translation", model=model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

#dictionary naten/future purposes pag magdadagdag ng new languages
dictionary = {
        'eng' : "eng_Latn",
        'ceb' : "ceb_Latn",
        'hili' : " "
}


#first install, initiate .dialecto app
def first_install():
    home_dir = os.path.expanduser("~") 
    app_dir = os.path.join(home_dir, ".dialecto_app")

    os.makedirs(app_dir, exist_ok=True)


#nllb dialecto modeel
def nllb_model(text):
    translator=pipeline('translation', model=model, tokenizer=tokenizer, src_lang=dictionary['eng'], tgt_lang=dictionary['ceb'], max_length = 400)
    translated_text = translator(text)
    return translated_text[0]['translation_text']


#deep translator (coounter checking}
def translate_deep(text):
    deeptrans = GoogleTranslator(source='auto',target='en')
    translated = deeptrans.translate(text)
    return translated


#recording directory
def get_app_audio_directory():
    """Creates and returns the app's dedicated directory."""
    home_dir = os.path.expanduser("~") 
    app_dir = os.path.join(home_dir, ".dialecto_app/audio")

    os.makedirs(app_dir, exist_ok=True) #cross-check if it exist
    return app_dir


#return latest recorded file
def get_latest():
    homedir = os.path.expanduser("~")
    audiodir = os.path.join(homedir,".dialecto_app/audio")

    files = [f for f in os.listdir(audiodir) if f.endswith(".wav")]
    if not files:
        print("No recordings found.")
        return None
    latest_recording = max(files,key = lambda f:os.path.getmtime(os.path.join(audiodir,f)))
    return os.path.join(audiodir,latest_recording)


def transtext(text):
        print(f"You said: {text}")
        print(f"(deeptranslate) translation:{translate_deep(text)}")
        print(f"(nllb_dialecto) translation:{nllb_model(text)}")
    


#recording start
def record_voice():
    """Records voice input and saves it in the app's directory."""
    save_folder = get_app_audio_directory()  # Get app directory

    while True:
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening... Speak now!")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                print(f"(deeptranslate) translation:{translate_deep(text)}")
                print(f"(nllb_dialecto) translation:{nllb_model(text)}")
                break
        except sr.UnknownValueError:
            print("Couldn't recognize audio, please try again")
        except sr.RequestError:
            print("Connection Prboelm")

        

        

    # Generate filename with timestamp
    print("==========================================================================================")
    filename = os.path.join(save_folder, f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")

    try:
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())

        print(f"Recording saved at: {filename}")
    except PermissionError:
        print(f"Permission denied: Unable to save file to {filename}. Try running as administrator.")





def main():
    first_install()
    while(True):
        op = input("""

    Dialecto v1.0 Console Beta
        
        1. translate audio cebuano to eng 
        2. translate cebuano text to eng 
        3. exit
        >> """ )

        match op:
            case "1":
                record_voice()
            case "2":
                text = input("input text you want to translate: ")
                transtext(text)
            case "3":
                print("exiting program")
                break
            case _:
                print("invalid error")
                return

        


 
if __name__ == "__main__":
    main()


