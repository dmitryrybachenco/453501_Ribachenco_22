import re
from .regex_patterns import RegexPatterns


class StringReplacer:
    """Class for replacing $v_(i) patterns with v[i]"""

    def __init__(self, text: str):
        """
        Initialize StringReplacer

        Args:
            text: Input text
        """
        self.original_text = text
        self.replaced_text = None

    def replace_v_pattern(self) -> str:
        """
        Replace all $v_(i) with v[i] where i is a single digit or letter

        Returns:
            Text with replacements
        """
        self.replaced_text = RegexPatterns.replace_v_pattern(self.original_text)
        return self.replaced_text

    def get_replaced_text(self) -> str:
        """Get the replaced text"""
        if self.replaced_text is None:
            self.replace_v_pattern()
        return self.replaced_text

    def print_comparison(self) -> None:
        """Print original and replaced text for comparison"""
        replaced = self.get_replaced_text()

        print(f"\nOriginal text:\n{self.original_text}")
        print(f"\nReplaced text:\n{replaced}")

        original_count = len(re.findall(r'\$v_\([a-zA-Z0-9]\)', self.original_text))
        print(f"\nNumber of replacements made: {original_count}")

    def find_all_matches(self) -> list:
        """Find all $v_(i) patterns in the text"""
        return re.findall(r'\$v_\(([a-zA-Z0-9])\)', self.original_text)