# APPA: AI Personal Performance Assistant
APPA is a custom-designed Raspberry Pi project that harnesses the power of various APIs to assist with day-to-day tasks. Inspired by Amazon's Alexa and Apple's Siri, APPA leverages OpenAI's ChatGPT model to answer questions and provide a range of functionalities.

## Features
- Weather Updates: Powered by OpenWeatherMap API
-Calendar Management: Integrated with Google Calendar API
- Music Streaming: Enabled via Spotify API
- Phone Messaging: Facilitated through Telegram Bot API
- Text-to-Speech: Utilizes OpenAI's text-to-speech API for a lifelike voice

## Project Main Structure
- main.py: The main script to run APPA.
- audio.py: Handles audio playback and text-to-speech functionalities.
- google_cal_api.py: Manages interactions with Google Calendar.
- openai_api.py: Connects to OpenAI's API for generating responses.
- spotify_api.py: Integrates with Spotify for music streaming.
- telegram_api.py: Manages Telegram Bot for sending messages.
- weather_api.py: Fetches weather data using OpenWeatherMap API.

## Example Usage
Give APPA a prompt
"Give a random fact"

APPA will categorize the prompt to decide which API to use
Category - General

Given the Category APPA will make an API call
General: prompt -> ChatGPT API -> reponse -> OpenAI text-to-speech API

Finally APPA will play the repsonse through the devices speakers

## How to Setup
Coming soon!

## Acknowledgements
- OpenAI for providing the ChatGPT model and text-to-speech API
- OpenWeatherMap for weather data
- Google for calendar integration
- Spotify for music streaming
- Telegram for messaging capabilities