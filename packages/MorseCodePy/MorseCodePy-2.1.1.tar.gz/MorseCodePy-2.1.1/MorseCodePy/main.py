import logging

from .codes import encodes, decodes, Language
from .extra import *

logging.basicConfig(format='%(levelname)s (%(asctime)s): %(message)s', datefmt='%d/%m %I:%M:%S %p',
                    level=logging.WARNING)

def encode(string: str, language: Language, dot: str = '.', dash: str = '-', separator: str = '/',
           error: str = '*') -> str:
    """
    Encodes your string into Morse code.

    :param string: The input string to be encoded.
    :param language: The language to use for encoding (e.g., Language.english, Language.french, Language.numbers).
    :param dot: The symbol to represent dots.
    :param dash: The symbol to represent dashes.
    :param separator: The symbol used to separate words.
    :param error: The symbol to represent errors when a character is not found in the dictionary.

    :return: The Morse code representation of the input string.
    """

    # Error handling: Ensure that dot, dash, and separator have only one symbol
    if any(len(symbol) != 1 for symbol in [dot, dash, separator]):
        logging.error(error_message1)
        return error_message1

    # Translating string into Morse code
    t_string: str = str()  # New string that will hold the translated text
    string = string.lower()  # Convert the input string to lowercase for consistent encoding

    char: int = 0
    while char != len(string):
        if string[char] == 'c' and string[char + 1] == 'h':
            # Special case for 'ch' in certain languages
            t_string += '1111'.replace('1', dash) + ' '
            char += 1
        elif string[char] == ' ':
            # Space character, add the separator to separate words
            t_string += separator + ' '
        elif string[char] in encodes[language]:
            # Character found in the selected language, encode it
            morse_code = encodes[language][string[char]]
            t_string += morse_code.replace('0', dot).replace('1', dash) + ' '
        elif string[char] in encodes[Language.numbers] and language != Language.special:
            # Character found in the numbers dictionary, encode it as a number
            morse_code = encodes[Language.numbers][string[char]]
            t_string += morse_code.replace('0', dot).replace('1', dash) + ' '
        elif string[char] in encodes[Language.special] and language != Language.numbers:
            # Character found in the special characters dictionary, encode it as a special character
            morse_code = encodes[Language.special][string[char]]
            t_string += morse_code.replace('0', dot).replace('1', dash) + ' '
        else:
            # Character not found in any dictionary, use the error symbol
            t_string += error + ' '

        char += 1

    return t_string.rstrip()


def decode(code: str, language: Language, dot: str = '.', dash: str = '-', separator: str = '/',
           error: str = '*') -> str:
    """
    Decode Morse code into a string.

    :param code: The input Morse code string to be decoded.
    :param language: The language to use for decoding (e.g., Language.english).
    :param dot: The symbol used to represent dots.
    :param dash: The symbol used to represent dashes.
    :param separator: The symbol used to separate words.
    :param error: The symbol to represent errors when an unknown Morse code sequence is encountered.

    :return: The decoded string.
    """

    # Error Handling: Ensure that dot, dash, and separator have only one symbol
    if any(len(symbol) != 1 for symbol in [dot, dash, separator]):
        logging.error(error_message1)
        return error_message1

    # Error Handling: Ensure that the input string contains only valid Morse code symbols
    if any(char not in dot + dash + separator + ' ' + '\n' for char in code):
        logging.error(error_message2)
        return error_message2

    # Separating String: Split the input Morse code into letters and separators
    letters: list = separate_words(words=code, dot=dot, dash=dash, separator=separator)

    # Translating Morse Code into normal text
    t_string: str = str()

    # Create dictionaries to map Morse code to characters for the selected language
    reversed_dictionary: dict = reverse_dictionary(decodes[language])
    reversed_numbers_dictionary: dict = reverse_dictionary(decodes[Language.numbers])
    reversed_special_dictionary: dict = reverse_dictionary(decodes[Language.special])

    # Create a mapping dictionary to translate Morse code symbols to '0' and '1'
    mapping: dict[str: str] = {dot: '0', dash: '1'}

    for letter in letters:
        # Translate Morse code symbols to '0' and '1'
        letter = str().join(mapping.get(char, char) for char in letter)

        if letter == '1111' and language in {Language.english, Language.spanish, Language.french}:
            # Special case for 'ch' in certain languages
            t_string += 'ch'
        elif letter == separator:
            # Separator, add a space to separate words
            t_string += ' '
        elif letter == '\n':
            # New line
            t_string += '\n'
        elif letter in reversed_dictionary:
            # Character found in the selected language, decode it
            t_string += reversed_dictionary[letter]
        elif letter in reversed_numbers_dictionary and language != Language.special:
            # Character found in the numbers dictionary, decode it as a number
            t_string += reversed_numbers_dictionary[letter]
        elif letter in reversed_special_dictionary and language != Language.numbers:
            # Character found in the special characters dictionary, decode it as a special character
            t_string += reversed_special_dictionary[letter]
        else:
            # Unknown Morse code sequence, use the error symbol
            t_string += error

    return t_string


def chart(dot: str = '·', dash: str = '-') -> None:
    """
    Print Morse code chart in the console.

    :param dot: The symbol to represent dots in the chart.
    :param dash: The symbol to represent dashes in the chart.

    :return: None
    """

    print('Morse Code Chart:')
    print('-' * 15)

    # Iterate through the language codes and their corresponding characters
    for language, codes in encodes.items():
        print(f'{language.name.capitalize()}:')

        # Print characters and their Morse code representations
        for char, code in codes.items():
            code = code.replace('0', dot).replace('1', dash)
            print(f"{char:<5} {code:<15}")

        print('-' * 15)


def play(code: str, delay: float = 0.4, dot: str = '.', dash: str = '-', separator: str = '/'):
    """
    Play Morse code sound.

    :param code: The Morse code string to play.
    :param delay: The delay in seconds between each Morse code symbol (default is 0.4).
    :param dot: Symbol representing a dot (default is '.').
    :param dash: Symbol representing a dash (default is '-').
    :param separator: Symbol representing a separator (default is '/').

    :return: None
    """

    # Error Handling: Ensure that dot, dash, and separator have only one symbol
    if any(len(symbol) != 1 for symbol in [dot, dash, separator]):
        logging.error(error_message1)
        return error_message1

    # Error Handling: Ensure that the input string contains only valid Morse code symbols
    if any(char not in dot + dash + separator + ' ' + '\n' for char in code):
        logging.error(error_message2)
        return error_message2

    # Separate the string into individual Morse code characters
    characters: list = separate_letters(separate_words(code, dot=dot, dash=dash, separator=separator, sound_mode=True))

    # Play Morse code
    for character in characters:
        match character:
            case '.':
                play_dot_sound()  # Play a dot sound
                sleep(delay / 1.7)  # Wait for the specified duration
            case '-':
                play_dash_sound()  # Play a dash sound
                sleep(delay)  # Wait for the specified duration
            case ' ':
                sleep(delay * 1.4)  # Wait for the specified duration for a space character
            case '/':
                sleep(delay * 2)  # Wait for the specified duration for a separator character
