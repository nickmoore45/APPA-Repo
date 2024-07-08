import os
from datetime import datetime
import threading
from assistant.audio import AudioRecorder
from assistant.speech_to_text import convert_audio_to_text
from assistant.openai_api import ask_chatgpt, text_to_speech
from assistant.google_cal_api import add_calendar_event
from assistant.calender_prompt import parse_calendar_prompt
from assistant.categorize_alg import categorize_prompt
from assistant.weather_api import get_weather
from assistant.spotify_api import SpotifyAPI
from assistant.music_info_alg import extract_music_info
from assistant.telegram_api import send_message
from hardware.led import light_up_all, sway_leds, cleanup, random_flash
from rpi_ws281x import Color
import pygame

pygame.mixer.init()

spotify = SpotifyAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUTWAV_PATH = os.path.join(BASE_DIR, 'audio/input.wav')
LONGMP3_PATH = os.path.join(BASE_DIR, 'audio/long_response.mp3')
APPAMP3_PATH = os.path.join(BASE_DIR, 'audio/APPA_YIPYIP.mp3')
FAILEDMP3_PATH = os.path.join(BASE_DIR, 'audio/failed.mp3')

def handle_calendar_command(response):
    summary = response["summary"]
    start_time_str = response["start_time"]
    end_time_string = response["end_time"]
    print(response["summary"] + " " + response["start_time"] + " " + response["end_time"])
    add_calendar_event(summary, start_time_str, end_time_string)
    print("Added to calendar.")
    text_to_speech(str(summary) + " has been added to your calendar.")

def on_recording_finished():
    print("Recording finished. Processing speech-to-text...")
    audio_path = INPUTWAV_PATH  
    text = convert_audio_to_text(audio_path)

    if text:
        text = text.lower()
        print(f"Transcribed Text: {text}")
        handle_command(text)
    else:
        print("No transcribed text available.")

def play_audio(file_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            random_flash()
        print("Playing speech with pygame.")
    except Exception as e:
        print(f"pygame failed to play audio: {e}")

def handle_command(text):
    sway_thread = threading.Thread(target=sway_leds)
    sway_thread.start()

    category = categorize_prompt(text) # find prompt category
    print(category)

    # Handle general commands to utilize openAI chatGPT model
    if category == "general":
        chatgpt_response = ask_chatgpt(text)
        if chatgpt_response:
            if len(chatgpt_response) < 700: #if response it too long, send telegram message instead
                print(f"ChatGPT Response: {chatgpt_response}")
                text_to_speech(chatgpt_response)
            else:
                send_message(chatgpt_response)
                play_audio(LONGMP3_PATH)
        return

    # Handle music commands to utilize spotify api
    if category == "music":
        spotify_command = text
        print("music command recognized")
        track, artist = extract_music_info(spotify_command) # deserialize

        if track and artist:
            query = f"{track} {artist}"
            search_result = spotify.search_track(query)
            if 'tracks' in search_result and 'items' in search_result['tracks'] and len(search_result['tracks']['items']) > 0:
                track_uri = search_result['tracks']['items'][0]['uri']
                
                devices = spotify.get_devices()
                if 'devices' in devices and len(devices['devices']) > 0:
                    device_id = devices['devices'][0]['id']

                    status_code, response = spotify.play_track(track_uri, device_id)
                    random_flash()

                    if status_code == 204:
                        print("Playback started")
                    else:
                        print(f"Error: {status_code}, {response}")
                else:
                    print("No devices available for playback.")
            else:
                print("No tracks found for the command.")
        else:
            print("Could not extract track or artist from the command.")

    # Handle calender commands to utilize google calender api
    elif category == "calendar":
        print("Calender prompt recognized")
        response = parse_calendar_prompt(text)
        handle_calendar_command(response)

    # Handle weather commands to utilize open weather map api
    elif category == "weather":
        print("Weather prompt recognized")
        weather = get_weather()
        response = ask_chatgpt("Simply humanize this weather outlook and round the temperatures: " + weather)
        print(response)
        text_to_speech(response)

    # appa yip yip
    elif category == "appa":
        print("appa yip yip")
        play_audio(APPAMP3_PATH)
    
    # anything else either failed or is not available yet.
    else:
        print("Command not recognized.")
        play_audio(FAILEDMP3_PATH)

    light_up_all(Color(255,255,255))

def main():
    light_up_all(Color(255,255,255))
    recorder = AudioRecorder()
    recorder.set_on_recording_finished(on_recording_finished)  # Set the callback
    print("System ready. Press the button to record.")
    
    try:
        recorder.run()
    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        recorder.cleanup()
        cleanup()

if __name__ == "__main__":
    main()
