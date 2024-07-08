from openai import OpenAI
import pygame
import os
from hardware.led import random_flash, light_up_all
from rpi_ws281x import Color
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('OPENAI_KEY')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTWAV_PATH = os.path.join(BASE_DIR, '../audio/output.mp3')


def ask_chatgpt(question_text):
    client = OpenAI(api_key=API_KEY)
    new_text = "In short tell me " + question_text
    print(new_text)
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Your name is appa, you are an artificial intelligence personal assistant"},
                {"role": "user", "content": question_text},
            ],
            model="gpt-3.5-turbo",
        )
        
        if chat_completion.choices:
            response_message = chat_completion.choices[0].message.content
            return response_message
        else:
            return "No response found."
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def text_to_speech(text):
    client = OpenAI(api_key=API_KEY)
    
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )

        # Save the speech to a file
        audio_content = response.read()
        with open(OUTPUTWAV_PATH, "wb") as audio_file:
            audio_file.write(audio_content)

        if os.path.exists(OUTPUTWAV_PATH) and os.path.getsize(OUTPUTWAV_PATH) > 0:
            try:
            
                pygame.mixer.init()
                pygame.mixer.music.load(OUTPUTWAV_PATH)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                    random_flash()
                print("Playing speech with pygame.")
            except Exception as e:
                print(f"pygame failed to play audio: {e}")
        else:
            print("Generated file is invalid or empty.")

        light_up_all(Color(255,255,255))
    except Exception as e:
        print(f"An error occurred while generating speech: {e}")

# Example usage
# if __name__ == "__main__":
#     question = "what temp should i smoke a brisket to"
#     response = "I'm sorry.   I didn't recognize that command, can you please repeat it?"
#     print(response)
#     text_to_speech(response)
