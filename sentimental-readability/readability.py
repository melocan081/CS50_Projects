from cs50 import get_string


def count_letters(text):
    number = 0
    for i in range(len(text)):
        if text[i].isalpha():
            number += 1
    return number


def count_words(text):
    number = 0
    for i in range(len(text)):
        if text[i] == " ":
            number += 1
    return number + 1


def count_sentences(text):
    number = 0
    for i in range(len(text)):
        if text[i] == "!" or text[i] == "." or text[i] == "?":
            number += 1
    return number


text = get_string("Enter text: ")

letters = count_letters(text)
words = count_words(text)
sentences = count_sentences(text)

L = (letters / words) * 100
S = (sentences / words) * 100


index = round((0.0588 * L) - (0.296 * S) - 15.8)

if 1 <= index < 16:
    print(f"Grade {str(index)}")
elif index >= 16:
    print("Grade 16+")
else:
    print("Before Grade 1")
