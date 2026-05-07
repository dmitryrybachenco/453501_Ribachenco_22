from typing import List, Dict
from .regex_patterns import RegexPatterns


class SentenceAnalyzer:
    """Class for sentence analysis"""

    def __init__(self, text: str):
        """
        Initialize SentenceAnalyzer

        Args:
            text: Input text to analyze
        """
        self.text = text
        self._sentences = None
        self._smileys_count = None
        self._smileys_list = None

    def get_sentences(self) -> List[str]:
        """Get list of sentences from text with punctuation preserved"""
        if self._sentences is None:
            self._sentences = RegexPatterns.split_sentences(self.text)
        return self._sentences

    def get_sentences_with_details(self) -> List[Dict]:
        """
        Get sentences with their types and lengths

        Returns:
            List of dicts with sentence, type, length, end punctuation
        """
        sentences = self.get_sentences()
        result = []

        for sentence in sentences:
            result.append({
                'text': sentence,
                'type': RegexPatterns.classify_sentence(sentence),
                'end_punctuation': RegexPatterns.get_sentence_end_punctuation(sentence),
                'word_count': len(RegexPatterns.find_all_words(sentence)),
                'char_count': len(sentence),
                'word_char_count': RegexPatterns.calculate_sentence_word_char_length(sentence)
            })

        return result

    def count_sentences(self) -> int:
        """Count total number of sentences"""
        return len(self.get_sentences())

    def classify_sentences(self) -> Dict[str, int]:
        """
        Classify sentences by type

        Returns:
            Dictionary with counts of declarative, interrogative, exclamatory sentences
        """
        sentences = self.get_sentences()
        counts = {
            'declarative': 0,    # повествовательные (заканчиваются на .)
            'interrogative': 0,  # вопросительные (заканчиваются на ?)
            'exclamatory': 0     # побудительные (заканчиваются на !)
        }

        for sentence in sentences:
            sent_type = RegexPatterns.classify_sentence(sentence)
            if sent_type:
                counts[sent_type] += 1

        return counts

    def print_sentence_types(self) -> None:
        """Print sentence type counts"""
        counts = self.classify_sentences()

        print(f"\nTotal sentences: {self.count_sentences()}")
        print(f"\nDeclarative (повествовательные): {counts['declarative']}")
        print(f"Interrogative (вопросительные): {counts['interrogative']}")
        print(f"Exclamatory (побудительные): {counts['exclamatory']}")

    def get_average_sentence_length(self) -> float:
        """
        Calculate average sentence length in characters (only words, not spaces/punctuation)

        Returns:
            Average sentence length
        """
        sentences = self.get_sentences()
        if not sentences:
            return 0.0

        total_word_chars = 0
        for sentence in sentences:
            total_word_chars += RegexPatterns.calculate_sentence_word_char_length(sentence)

        return total_word_chars / len(sentences)

    def get_average_sentence_length_with_spaces(self) -> float:
        """
        Calculate average sentence length including spaces and punctuation

        Returns:
            Average sentence length
        """
        sentences = self.get_sentences()
        if not sentences:
            return 0.0

        total_length = sum(len(s) for s in sentences)
        return total_length / len(sentences)

    def get_average_word_length(self) -> float:
        """
        Calculate average word length in characters

        Returns:
            Average word length
        """
        word_lengths = RegexPatterns.get_word_lengths(self.text)
        if not word_lengths:
            return 0.0

        return sum(word_lengths) / len(word_lengths)

    def count_smileys(self) -> int:
        """
        Count smileys in text

        Returns:
            Number of smileys
        """
        if self._smileys_count is None:
            self._smileys_count = RegexPatterns.count_smileys(self.text)
        return self._smileys_count

    def get_smileys_list(self) -> list:
        """Get list of all smileys found in text"""
        if self._smileys_list is None:
            self._smileys_list = RegexPatterns.find_all_smileys(self.text)
        return self._smileys_list

    def print_sentence_statistics(self) -> None:
        """Print all sentence statistics"""
        sentences = self.get_sentences()

        print(f"\nTotal sentences: {self.count_sentences()}")
        print(f"Average sentence length (word chars only): {self.get_average_sentence_length():.2f}")
        print(f"Average sentence length (with punctuation): {self.get_average_sentence_length_with_spaces():.2f}")
        print(f"Average word length: {self.get_average_word_length():.2f}")
        print(f"Number of smileys: {self.count_smileys()}")

    def get_complete_sentence_stats(self) -> Dict:
        """
        Get complete sentence statistics as dictionary

        Returns:
            Dictionary with all sentence statistics
        """
        sentence_counts = self.classify_sentences()
        sentences_with_details = self.get_sentences_with_details()

        return {
            'total_sentences': self.count_sentences(),
            'declarative_count': sentence_counts['declarative'],
            'interrogative_count': sentence_counts['interrogative'],
            'exclamatory_count': sentence_counts['exclamatory'],
            'avg_sentence_length': self.get_average_sentence_length(),
            'avg_sentence_length_with_punctuation': self.get_average_sentence_length_with_spaces(),
            'avg_word_length': self.get_average_word_length(),
            'smiley_count': self.count_smileys(),
            'smileys_list': self.get_smileys_list(),
            'sentences_list': self.get_sentences(),
            'sentences_with_details': sentences_with_details
        }