import re

def categorize_prompt(prompt):
    prompt = prompt.lower()
    
    weather_keywords = re.compile(r"\b(weather|temperature|forecast|rain|snow|sunny|cloudy|wind|humidity|storm|hail)\b")
    spotify_keywords = re.compile(r"\b(spotify|play|song|music|playlist|track|album|artist)\b")
    calendar_keywords = re.compile(r"\b(calendar|schedule|event|appointment|reminder|meeting|task|date|time)\b")
    appa_keywords = re.compile(r"\b(apa|abba|yip|yep)\b")
    
    
    # Check for specific phrases indicating a weather question
    if re.search(weather_keywords, prompt):
        return "weather"
    
    # Check for specific phrases indicating a music request
    elif re.search(spotify_keywords, prompt):
        return "music"
    
    # Check for specific phrases indicating a calendar request
    elif re.search(calendar_keywords, prompt):
        return "calendar"
    
    # Check for specific phrases indicating a good ol yip yip
    elif re.search(appa_keywords, prompt):
        return "appa"
    
    # Default to general question
    return "general"

# tests
# prompts = [
#     "Can you add a meeting to my calendar tomorrow?",
#     "What's the weather like today?",
#     "Play my favorite song on Spotify.",
#     "What is the capital of France?",
#     "Schedule an appointment for next week.",
#     "Is it going to rain tomorrow?",
#     "Play some jazz music.",
#     "When is my next meeting?",
#     "Tell me something new",
#     "appa yip yip"
# ]

# for prompt in prompts:
#     category = categorize_prompt(prompt)
#     print(f"Prompt: {prompt}\nCategory: {category}\n")
