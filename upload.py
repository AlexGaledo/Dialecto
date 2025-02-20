import speech_recognition as sr
from pydub import AudioSegment
import os

def get_audio_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:  # FIXED: Instantiate Microphone
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        # Define file paths
        raw_audio_dir = "/raw_audio"
        os.makedirs(raw_audio_dir, exist_ok=True)  # Create directory if not exists
        
        wav_file_path = os.path.join(raw_audio_dir, "recorded_audio.wav")
        mp3_file_path = os.path.join(raw_audio_dir, "recorded_audio.mp3")

        try:
        # Save recorded audio as WAV
            with open(wav_file_path, "wb") as f:
                f.write(audio.get_wav_data())

            print(f"Audio saved as WAV: {wav_file_path}")

            # Convert to MP3
            sound = AudioSegment.from_wav(wav_file_path)
            sound.export(mp3_file_path, format="mp3")

            print(f"Audio converted to MP3: {mp3_file_path}")
        except PermissionError:
            print("permission error")

get_audio_input()
