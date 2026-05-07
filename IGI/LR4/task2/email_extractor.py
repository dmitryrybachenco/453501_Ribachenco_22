from typing import List, Tuple, Optional
from .regex_patterns import RegexPatterns


class EmailExtractor:
    """Class for extracting emails and names from text"""

    def __init__(self, text: str):
        """
        Initialize EmailExtractor

        Args:
            text: Input text to analyze
        """
        self.text = text
        self._emails = None

    def extract_all_emails(self) -> List[Tuple[Optional[str], str]]:
        """
        Extract all emails with their corresponding names

        Returns:
            List of tuples (name, email) where name may be None
        """
        self._emails = RegexPatterns.extract_emails(self.text)
        return self._emails

    def print_emails_with_names(self) -> None:
        """Print emails with their corresponding names"""
        if self._emails is None:
            self.extract_all_emails()

        if not self._emails:
            print("No emails found in the text.")
            return

        for i, (name, email) in enumerate(self._emails, 1):
            if name:
                print(f"{i}. Name: {name}")
                print(f"   Email: {email}")
            else:
                print(f"{i}. Email: {email} (no associated name)")
            print()