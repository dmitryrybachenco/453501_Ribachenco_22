from .email_extractor import EmailExtractor
from .string_replacer import StringReplacer
from .text_analyzer import TextAnalyzer
from .sentence_analyzer import SentenceAnalyzer
from .file_processor import FileProcessor

def demonstrate_email_extraction(text: str) -> list:
    """Demonstrate email extraction functionality"""
    print("\n" + "=" * 70)
    print("1. EMAIL EXTRACTION")
    print("=" * 70)

    extractor = EmailExtractor(text)
    extractor.print_emails_with_names()

    return extractor.extract_all_emails()


def demonstrate_string_replacement(text: str) -> tuple:
    """Demonstrate string replacement functionality"""
    print("\n" + "=" * 70)
    print("2. STRING REPLACEMENT: $v_(i) -> v[i]")
    print("=" * 70)

    replacer = StringReplacer(text)
    replacer.print_comparison()

    return replacer.get_replaced_text(), replacer.find_all_matches()


def demonstrate_vowel_words_analysis(text: str) -> dict:
    """Demonstrate vowel words analysis"""
    print("\n" + "=" * 70)
    print("3. WORDS STARTING OR ENDING WITH VOWELS")
    print("=" * 70)

    analyzer = TextAnalyzer(text)
    analyzer.print_vowel_words_analysis()

    count, words = analyzer.count_words_starting_or_ending_with_vowel()
    return {
        'total_words': len(analyzer.get_all_words()),
        'vowel_words_count': count,
        'vowel_words': words
    }


def demonstrate_character_frequency(text: str) -> dict:
    """Demonstrate character frequency analysis"""
    print("\n" + "=" * 70)
    print("4. CHARACTER FREQUENCY")
    print("=" * 70)

    analyzer = TextAnalyzer(text)
    analyzer.print_character_frequency()

    return analyzer.get_character_frequency()


def demonstrate_words_after_comma(text: str) -> list:
    """Demonstrate words after comma analysis"""
    print("\n" + "=" * 70)
    print("5. WORDS AFTER COMMA (Alphabetical Order)")
    print("=" * 70)

    analyzer = TextAnalyzer(text)
    analyzer.print_words_after_comma()

    return analyzer.get_words_after_comma_sorted()


def demonstrate_sentence_statistics(text: str) -> dict:
    """Demonstrate sentence statistics"""
    print("\n" + "=" * 70)
    print("6. GENERAL TEXT STATISTICS")
    print("=" * 70)

    sentence_analyzer = SentenceAnalyzer(text)
    sentence_analyzer.print_sentence_types()
    sentence_analyzer.print_sentence_statistics()

    return sentence_analyzer.get_complete_sentence_stats()


def run_full_analysis(text: str, processor: FileProcessor) -> None:
    """Run all analysis and save results"""

    emails = demonstrate_email_extraction(text)
    replaced_text, v_matches = demonstrate_string_replacement(text)
    text_analysis_results = demonstrate_vowel_words_analysis(text)
    char_freq = demonstrate_character_frequency(text)
    comma_words = demonstrate_words_after_comma(text)
    sentence_stats = demonstrate_sentence_statistics(text)

    text_analysis_dict = {
        'total_words': text_analysis_results['total_words'],
        'vowel_words_count': text_analysis_results['vowel_words_count'],
        'vowel_words': text_analysis_results['vowel_words'],
        'character_frequency': char_freq,
        'words_after_comma': comma_words
    }

    processor.save_results_to_file(
        text=text,
        email_results=emails,
        replaced_text=replaced_text,
        v_matches=v_matches,
        text_analysis=text_analysis_dict,
        sentence_stats=sentence_stats
    )

    processor.create_archive()


def main():
    """Main function for Task 2"""
    print("\n" + "=" * 70)
    print("LABORATORY WORK No. 4 - TASK 2 (VARIANT 22)")
    print("Email Extraction | String Replacement | Text Analysis")
    print("=" * 70)

    input_file = "input_text_v22.txt"
    output_file = "analysis_results_v22.txt"

    processor = FileProcessor(input_file, output_file)
    text = processor.read_text_from_file()

    run_full_analysis(text, processor)

    print("\n" + "=" * 70)
    print("Task 2 completed successfully!")
    print("=" * 70)