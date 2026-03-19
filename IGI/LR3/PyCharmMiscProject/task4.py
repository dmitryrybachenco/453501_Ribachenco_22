"""
Task 4: Text analysis of Alice in Wonderland excerpt.
Author: Ribachenko Dmitriy
Date: 18.03.2026
"""

from typing import Tuple
import utils
import string

ALICE_TEXT = """So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, 
                whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, 
                when suddenly a White Rabbit with pink eyes ran close by her."""


def count_lowercase_letters(text: str) -> int:
    """
    Count lowercase letters in text.
    """
    count = 0
    for char in text:
        if char.islower():
            count += 1
    return count


def find_last_word_with_i(text: str) -> Tuple[str, int]:
    """
    Find the last word containing letter 'i'.
    """
    words = []
    for word in text.split():
        clean_word = word.strip(string.punctuation)
        if clean_word:
            words.append(clean_word)

    last_word = None
    last_index = -1

    for i, word in enumerate(words, 1):
        if 'i' in word.lower():
            last_word = word
            last_index = i

    return last_word, last_index


def remove_words_starting_with_i(text: str) -> str:
    """
    Remove words starting with 'a' or 'A' from text.
    """
    words = text.split()
    result_words = []

    for word in words:
        clean_word = word.strip(string.punctuation)
        if clean_word and not clean_word.lower().startswith('i'):
            result_words.append(word)

    return ' '.join(result_words)


@utils.decorator_repeat
def analyze_text() -> None:
    """Perform all analyses on the given text."""

    print("\n" + "=" * 60)
    print("TEXT FOR ANALYSIS:")
    print("-" * 60)
    print(ALICE_TEXT)
    print("=" * 60)

    lowercase_count = count_lowercase_letters(ALICE_TEXT)
    print(f"\na) Number of lowercase letters: {lowercase_count}")

    last_word, position = find_last_word_with_i(ALICE_TEXT)
    if last_word:
        print(f"b) Last word containing 'i': '{last_word}' (position: {position})")
    else:
        print("b) No word containing 'i' found.")

    modified_text = remove_words_starting_with_i(ALICE_TEXT)
    print(f"c) Text with words starting with 'a' removed:")
    print("-" * 40)
    print(modified_text)


def run_task4() -> None:
    """Main function to run Task 4."""
    print("\n" + "=" * 60)
    print("TASK 4: TEXT ANALYSIS (VARIANT 22)")
    print("=" * 60)

    analyze_text()