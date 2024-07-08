import speech_recognition as sr

def convert_audio_to_text(audio_path):
  
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    
    text = None
    try:
        print("trying speech to text")
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    return text


