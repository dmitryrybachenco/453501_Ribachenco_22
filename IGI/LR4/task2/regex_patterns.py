import re


class RegexPatterns:
    """Container class for regex patterns"""

    EMAIL_WITH_NAME = r'([A-Za-z\s]+)\s*<([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})>'
    EMAIL_ONLY = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

    V_PATTERN = r'\$v_\(([a-zA-Z0-9])\)'

    WORD_PATTERN = r'\b\w+\b'

    ENGLISH_VOWELS = set('aeiouyAEIOUY')
    RUSSIAN_VOWELS = set('аеёиоуыэюяАЕЁИОУЫЭЮЯ')
    ALL_VOWELS = ENGLISH_VOWELS | RUSSIAN_VOWELS

    SENTENCE_SPLIT_PATTERN = r'(?<=[.!?])\s+(?=[A-ZА-ЯЁ"\'\(])'

    SENTENCE_END_PATTERN = r'[.!?]'

    COMPLETE_SENTENCE_PATTERN = r'[^.!?]*[.!?]+'

    DECLARATIVE_END = r'\.$'
    INTERROGATIVE_END = r'\?$'
    EXCLAMATORY_END = r'!$'

    SMILEY_PATTERN = r'[;:]-*[\(\)\[\]]+'

    @classmethod
    def extract_emails(cls, text: str) -> list:
        """Extract emails with corresponding names"""
        results = []

        matches = re.findall(cls.EMAIL_WITH_NAME, text)
        for name, email in matches:
            results.append((name.strip(), email))

        emails_without_names = re.findall(cls.EMAIL_ONLY, text)
        for email in emails_without_names:
            if not any(email == e for _, e in results):
                results.append((None, email))

        return results

    @classmethod
    def replace_v_pattern(cls, text: str) -> str:
        """Replace $v_(i) with v[i]"""
        return re.sub(cls.V_PATTERN, r'v[\1]', text)

    @classmethod
    def find_all_words(cls, text: str) -> list:
        """Find all words in text"""
        return re.findall(cls.WORD_PATTERN, text)

    @classmethod
    def starts_or_ends_with_vowel(cls, word: str) -> bool:
        """Check if word starts or ends with a vowel"""
        if not word:
            return False
        return (word[0] in cls.ALL_VOWELS or word[-1] in cls.ALL_VOWELS)

    @classmethod
    def get_words_after_comma(cls, text: str) -> list:
        """Get words that appear after commas"""
        words_after_comma = []
        parts = re.split(r',\s*', text)

        for part in parts[1:]:
            words = re.findall(cls.WORD_PATTERN, part)
            if words:
                words_after_comma.append(words[0])

        return words_after_comma

    @classmethod
    def split_sentences(cls, text: str) -> list:
        """
        Split text into sentences while preserving punctuation

        This method properly splits text at sentence boundaries (. ! ?)
        while keeping the punctuation marks at the end of each sentence.

        Args:
            text: Input text

        Returns:
            List of sentences with punctuation preserved
        """
        if not text:
            return []

        sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZА-ЯЁ"\'\(]|$)', text.strip())

        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            sentences = re.findall(r'[^.!?]*[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]

        return sentences

    @classmethod
    def classify_sentence(cls, sentence: str) -> str:
        """
        Classify sentence type based on ending punctuation

        Returns:
            'declarative' - ends with . (повествовательное)
            'interrogative' - ends with ? (вопросительное)
            'exclamatory' - ends with ! (побудительное)
        """
        sentence = sentence.strip()
        if not sentence:
            return None

        # Check last character
        if sentence.endswith('?'):
            return 'interrogative'
        elif sentence.endswith('!'):
            return 'exclamatory'
        elif sentence.endswith('.'):
            return 'declarative'
        else:
            return 'declarative'

    @classmethod
    def get_sentence_end_punctuation(cls, sentence: str) -> str:
        """Extract the ending punctuation of a sentence"""
        sentence = sentence.strip()
        if sentence.endswith('?'):
            return '?'
        elif sentence.endswith('!'):
            return '!'
        elif sentence.endswith('.'):
            return '.'
        return ''

    @classmethod
    def count_smileys(cls, text: str) -> int:
        """Count smileys in text"""
        smileys = re.findall(cls.SMILEY_PATTERN, text)
        return len(smileys)

    @classmethod
    def find_all_smileys(cls, text: str) -> list:
        """Find all smileys with their positions"""
        return [(m.group(), m.start()) for m in re.finditer(cls.SMILEY_PATTERN, text)]

    @classmethod
    def get_word_lengths(cls, text: str) -> list:
        """Get list of word lengths"""
        words = cls.find_all_words(text)
        return [len(word) for word in words]

    @classmethod
    def calculate_sentence_word_char_length(cls, sentence: str) -> int:
        """
        Calculate total characters in words of a sentence (excluding spaces and punctuation)

        Args:
            sentence: Input sentence

        Returns:
            Total number of characters in all words
        """
        words = cls.find_all_words(sentence)
        return sum(len(word) for word in words)