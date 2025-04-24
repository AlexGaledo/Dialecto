import backend.app as fd

# Deep Translator (counter checking)
def translate_deep(text):
    deeptrans = fd.GoogleTranslator(source='auto', target='en')
    translated = deeptrans.translate(text)
    return translated


# Recording directory
def get_app_audio_directory():
    """Creates and returns the app's dedicated directory."""
    home_dir = fd.os.path.expanduser("~") 
    app_dir = fd.os.path.join(home_dir, ".dialecto_app/audio")

    fd.os.makedirs(app_dir, exist_ok=True)  # Ensure directory exists
    return app_dir


# Return latest recorded file
def get_latest():
    homedir = fd.os.path.expanduser("~")
    audiodir = fd.os.path.join(homedir, ".dialecto_app/audio")

    files = [f for f in fd.os.listdir(audiodir) if f.endswith(".wav")]
    if not files:
        print("No recordings found.")
        return None
    latest_recording = max(files, key=lambda f: fd.os.path.getmtime(fd.os.path.join(audiodir, f)))
    return fd.os.path.join(audiodir, latest_recording)


# Text Translation
def transtext(text, direction):
    print(f"You said: {text}")
    print(f"(deeptranslate) translation: {translate_deep(text)}")
    print(f"(nllb_dialecto) translation: {fd.nllb_model(text, direction)}")


# Recording Start
def record_voice(direction):
    """Records voice input and saves it in the app's directory."""
    save_folder = get_app_audio_directory()

    while True:
        try:
            recognizer = fd.sr.Recognizer()
            with fd.sr.Microphone() as source:
                print("Listening... Speak now!")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)

                print(f"You said: {text}")
                print(f"(deeptranslate) translation: {translate_deep(text)}")
                print(f"(nllb_dialecto) translation: {fd.nllb_model(text, direction)}")
                break

        except fd.sr.UnknownValueError:
            print("Couldn't recognize audio, please try again.")
        except fd.sr.RequestError:
            print("Connection Problem")

    # Generate filename with timestamp
    print("=" * 90)
    filename = fd.os.path.join(save_folder, f"recording_{fd.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")

    try:
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())

        print(f"Recording saved at: {filename}")
    except PermissionError:
        print(f"Permission denied: Unable to save file to {filename}. Try running as administrator.")