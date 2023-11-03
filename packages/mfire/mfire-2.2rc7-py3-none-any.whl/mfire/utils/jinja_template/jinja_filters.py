def letter_is_vowel(letter: str) -> bool:
    letter = letter.upper()
    return True if letter in ["A", "E", "I", "O", "U", "Y"] else False


def prefix_by_de_or_d(input_str: str):
    if letter_is_vowel(input_str[0]):
        return f"d'{input_str}"
    return f"de {input_str}"
