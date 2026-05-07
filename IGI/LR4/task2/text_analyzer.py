from collections import Counter
from typing import List, Dict, Tuple
from .regex_patterns import RegexPatterns


class TextAnalyzer:
    """Class for text analysis"""

    def __init__(self, text: str):
        """
        Initialize TextAnalyzer

        Args:
            text: Input text to analyze
        """
        self.text = text
        self._words = None
        self._char_frequency = None

    def get_all_words(self) -> List[str]:
        """Get all words from text"""
        if self._words is None:
            self._words = RegexPatterns.find_all_words(self.text)
        return self._words

    def count_words_starting_or_ending_with_vowel(self) -> Tuple[int, List[str]]:
        """
        Count words that start or end with a vowel

        Returns:
            Tuple (count, list_of_words)
        """
        words = self.get_all_words()
        vowel_words = []

        for word in words:
            if RegexPatterns.starts_or_ends_with_vowel(word):
                vowel_words.append(word)

        return len(vowel_words), vowel_words

    def get_character_frequency(self) -> Dict[str, int]:
        """
        Count frequency of each character in the text

        Returns:
            Dictionary with characters as keys and counts as values
        """
        if self._char_frequency is None:
            self._char_frequency = Counter(self.text)
        return dict(self._char_frequency)

    def print_character_frequency(self) -> None:
        """Print character frequency in a formatted way"""
        freq = self.get_character_frequency()

        if not freq:
            print("No characters found.")
            return

        sorted_freq = sorted(freq.items())

        print("\nCharacter | Count")
        print("-" * 30)
        for char, count in sorted_freq:
            display_char = repr(char)[1:-1] if char in '\n\t\r ' else char
            print(f"   {display_char:^8} | {count}")

        print(f"\nTotal unique characters: {len(freq)}")
        print(f"Total characters (including spaces): {sum(freq.values())}")

    def get_words_after_comma_sorted(self) -> List[str]:
        """
        Get words that appear after commas, sorted alphabetically

        Returns:
            Sorted list of words after commas
        """
        words = RegexPatterns.get_words_after_comma(self.text)
        return sorted(set(words))

    def print_words_after_comma(self) -> None:
        """Print words after comma in alphabetical order"""
        words = self.get_words_after_comma_sorted()

        if not words:
            print("No words found after commas.")
            return

        print("\n" + ", ".join(words))
        print(f"\nTotal unique words: {len(words)}")

    def print_vowel_words_analysis(self) -> None:
        """Print analysis of words starting or ending with vowels"""
        count, words = self.count_words_starting_or_ending_with_vowel()

        print(f"\nTotal words in text: {len(self.get_all_words())}")
        print(f"Words starting or ending with vowel: {count}")