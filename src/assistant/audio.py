import time
import os
from gpiozero import Button
import pyaudio
import wave
from rpi_ws281x import Color
from hardware.led import light_up_all, color_fade
from assistant.spotify_api import SpotifyAPI

spotify = SpotifyAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUTWAV_PATH = os.path.join(BASE_DIR, '../audio/input.wav')

class AudioRecorder:
    def __init__(self):
        self.button = Button(17) 
        
        # Audio setup
        self.chunk = 4096
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.wave_output_filename = INPUTWAV_PATH
        self.audio = pyaudio.PyAudio()

        self.button.when_pressed = self.start_recording

        # Callback
        self.on_recording_finished = None

    def start_recording(self):
        spotify.get_playback_state()
        if spotify.is_playing:
            print("Pausing playback...")
            devices = spotify.get_devices()
            if 'devices' in devices and len(devices['devices']) > 0:
                device_id = devices['devices'][0]['id']
                status_code, response = spotify.pause_playback(device_id)
                if status_code == 204:
                    print("Playback paused")
                else:
                    print(f"Error: {status_code}, {response}")
            else:
                print("No devices available to pause playback.")

        print("Recording...")
        color_fade((255, 255, 255), (0, 255, 0), duration=.25)

        frames = []
        stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        
        try:
            while self.button.is_pressed:
                try:
                    data = stream.read(self.chunk, exception_on_overflow=False)
                    frames.append(data)
                except IOError as e:
                    print(f"Buffer overflow handled: {e}")
        finally:
            stream.stop_stream()
            stream.close()

        wf = wave.open(self.wave_output_filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        print("Recording stopped.")
        color_fade((0, 255, 0), (255, 255, 255), duration=.25)

        self._finish_recording()  

        time.sleep(3)

    def set_on_recording_finished(self, callback):
        self.on_recording_finished = callback

    def _finish_recording(self):
        if self.on_recording_finished is not None:
            self.on_recording_finished()

    def run(self):
        print("System ready. Press the button to record.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
            self.cleanup()

    def cleanup(self):
        self.audio.terminate()

if __name__ == "__main__":
    recorder = AudioRecorder()
    recorder.run()
