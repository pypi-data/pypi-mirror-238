
<img alt="Logo" src="https://images2.imgbox.com/a2/44/Xcip287L_o.png" width="350"/>

![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue)
![PyGame Version](https://img.shields.io/badge/PyGame-2.5.2%2B-red)


## Introduction
**MorseCodePy** is a versatile Python module that streamlines the **encoding** and **decoding**
of text into Morse code and back. With support for multiple languages, including **English**, **Russian**, **Ukrainian**
**Spanish**, **French**, as well as provisions for handling **numbers** and other **special characters**, this module
offers a powerful and **user-friendly** Morse code tool. Whether you want to send messages, decipher
existing ones, or simply explore the world of Morse code, **MorseCodePy** has you covered.
___

## How to Use

#### `encode(string, language, dot, dash, error)`
Encode a text string into Morse code.

- `string`: The text string you want to encode.
- `language`: The target language for encoding (e.g., `Language.english`, `Language.french`, `Language.numbers`).
- `dot`: *(optional)* Symbol to represent dots (default is `.`).
- `dash`: *(optional)* Symbol to represent dashes (default is `-`).
- `error`: *(optional)* Symbol to represent errors when an unknown character is encountered (default is `*`).

```python
from MorseCodePy import encode, Language

encoded_string = encode('Hello, world!', language=Language.english)
print(encoded_string)
# Output: .... . .-.. .-.. --- --..-- / .-- --- .-. .-.. -.. -.-.--
```
___

#### `decode(code, language, dot, dash, error)`
Decode Morse code into a text string.

- `code`: The Morse code string you want to decode.
- `language`: The target language for decoding (e.g., `Language.russian`, `Language.spanish`, `Language.special`).
- `dot`: *(optional)* Symbol to represent dots (default is `.`).
- `dash`: *(optional)* Symbol to represent dashes (default is `-`).
- `error`: *(optional)* Symbol to represent errors when an unknown Morse code sequence is encountered (default is `*`).

```python
from MorseCodePy import decode, Language

decoded_string = decode('···· · ·-·· ·-·· --- --··-- / ·-- --- ·-· ·-·· -·· -·-·--', language=Language.english, dot='·')
print(decoded_string)
# Output: hello, world!
```
___

#### `Language`
The `Language` enumeration represents different languages, including special cases for numbers and special characters.
Use it to specify the language when encoding or decoding Morse code.

Supported languages include `Language.english`, `Language.spanish`, `Language.french`, `Language.russian`, `Language.ukrainian`,
as well as special categories for handling `Language.numbers` and `Language.special`.
___

#### `chart(dot, dash)`
Print a Morse code chart in the console.

- `dot`: *(optional)* Symbol to represent dots (default is `·`).
- `dash`: *(optional)* Symbol to represent dashes (default is `-`).

```python
from MorseCodePy import chart

chart()
# Output: Morse Code Chart: ...
```
___

#### `play(code, delay, dot, dash, separator)`
Play Morse code sound.

- `code`: The Morse code you want to play.
- `delay`: *(optional)* The delay in seconds between characters (default is **0.5**).
- `dot`: *(optional)* Symbol to represent dots (default is `.`).
- `dash`: *(optional)* Symbol to represent dashes (default is `-`).
- `separator`: *(optional)* Symbol to represent separators (default is `/`).

```python
from MorseCodePy import encode, Language, play

encoded_string: str = encode('Hello', language=Language.english)

play(encoded_string, delay=0.5)
```
___

#### `encodes` and `decodes`
These dictionaries contain Morse code representations for various languages and characters.
You can access these dictionaries to customize the encoding and decoding behavior.

```python
import MorseCodePy as mcp

english_encoding = mcp.encodes[mcp.Language.english]
russian_decoding = mcp.decodes[mcp.Language.russian]
```
___

## Licence
This project is licensed under the **MIT License**.
___

## Contact
- **[Discord](https://discord.com/users/873920068571000833)**
- [Email](mailto:karpenkoartem2846@gmail.com)
- [GitHub](https://github.com/CrazyFlyKite)
