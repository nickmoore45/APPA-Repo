import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_music_info(command):
    command = re.sub(r'can you play|play|on spotify|please', '', command, flags=re.I).strip()

    doc = nlp(command)

    track = ""
    artist = ""

    for ent in doc.ents:
        if ent.label_ == "WORK_OF_ART":
            track = ent.text
        elif ent.label_ == "PERSON":
            artist = ent.text

    if not track or not artist:
        match = re.search(r'(?P<track>.+?) by (?P<artist>.+)', command, re.I)
        if match:
            track = match.group('track').strip()
            artist = match.group('artist').strip()

    return track, artist

# Example usage:
# command1 = "Can you play A Team by Ed Sheeran?"
# command2 = "Play Ring of Fire by Johnny Cash on Spotify"

# print(extract_music_info(command1))  # Output: ('A Team', 'Ed Sheeran')
# print(extract_music_info(command2))  # Output: ('Ring of Fire', 'Johnny Cash')