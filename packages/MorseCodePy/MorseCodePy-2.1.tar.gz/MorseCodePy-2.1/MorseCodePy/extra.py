# Hide the pygame support prompt
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Import necessary modules
from pygame import mixer
from time import sleep

# Define error messages
error_message1: str = 'Invalid symbols: Dots, dashes, and separators must be single characters!'
error_message2: str = 'Invalid characters in the Morse code string. Use only specified dots, dashes, spaces, and separators!'

# Initialize the pygame mixer
mixer.init()

# Function to play the dot sound
def play_dot_sound() -> None:
    mixer.music.load(r'sounds/Dot.wav')  # Load the Dot.wav sound file
    mixer.music.play()  # Play the sound
    sleep(0.09)  # Add a short delay to simulate the duration of a dot

# Function to play the dash sound
def play_dash_sound() -> None:
    mixer.music.load(r'sounds/Dash.wav')  # Load the Dash.wav sound file
    mixer.music.play()  # Play the sound
    sleep(0.24)  # Add a short delay to simulate the duration of a dash

# Function to separate words into Morse code letters
def separate_words(words: str, dot: str, dash: str, separator: str, sound_mode: bool = False) -> list:
    letters: list = list()
    current_element: str = str()

    for char in words:
        if char in (dot, dash):
            current_element += char
        elif char == separator:
            if current_element:
                letters.append(current_element)
                current_element = str()
            letters.append(separator)
        elif char == ' ':
            if current_element:
                letters.append(current_element)
                current_element = str()
            if sound_mode is True:
                letters.append(' ')
        else:
            current_element += char

    if current_element:
        letters.append(current_element)

    return letters

# Function to separate Morse code letters
def separate_letters(letters: list):
    return [char for letter in letters for char in letter]

# Function to reverse the keys and values of a dictionary
def reverse_dictionary(dictionary: dict) -> dict:
    return {v: k for k, v in dictionary.items()}
