import re

def main():
    text = input("Text: ")

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    grade = calculate_grade(letters, words, sentences)

    if grade >= 16:
        print("Grade 16+")
    elif grade < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {grade}")


def count_letters(text):
    """Count the number of letters in the text."""
    return sum(1 for char in text if char.isalpha())


def count_words(text):
    """Count the number of words in the text."""
    return len(text.split())


def count_sentences(text):
    """Count the number of sentences in the text."""
    return sum(1 for char in text if char in ".!?")


def calculate_grade(letters, words, sentences):
    """Calculate the Coleman-Liau index."""
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    return round(index)


if __name__ == "__main__":
    main()
