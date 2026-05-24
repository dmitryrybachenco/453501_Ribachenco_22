import zipfile
import os
from datetime import datetime
from typing import Optional, Dict


class FileProcessor:
    """Class for file operations including archiving"""

    def __init__(self, input_file: str, output_file: str):
        """
        Initialize FileProcessor

        Args:
            input_file: Path to input file
            output_file: Path to output file for results
        """
        self.input_file = input_file
        self.output_file = output_file
        self.archive_name = output_file.replace('.txt', '.zip')

    def read_text_from_file(self) -> Optional[str]:
        """
        Read text from input file

        Returns:
            Text content or None if error
        """
        try:
            with open(self.input_file, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File '{self.input_file}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def save_results_to_file(self, text: str,
                             email_results: list,
                             replaced_text: str,
                             v_matches: list,
                             text_analysis: Dict,
                             sentence_stats: Dict) -> bool:
        """
        Save all analysis results to output file

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.output_file, 'w', encoding='utf-8') as file:
                file.write("=" * 80 + "\n")
                file.write("LABORATORY WORK No. 4 - TASK 2 (VARIANT 22)\n")
                file.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("=" * 80 + "\n\n")

                file.write("=" * 80 + "\n")
                file.write("1. ORIGINAL TEXT\n")
                file.write("=" * 80 + "\n")
                file.write(text + "\n\n")

                file.write("=" * 80 + "\n")
                file.write("2. EMAIL EXTRACTION\n")
                file.write("=" * 80 + "\n")
                if email_results:
                    for i, (name, email) in enumerate(email_results, 1):
                        if name:
                            file.write(f"{i}. Name: {name}\n")
                            file.write(f"   Email: {email}\n\n")
                        else:
                            file.write(f"{i}. Email: {email}\n\n")
                else:
                    file.write("No emails found.\n\n")

                file.write("=" * 80 + "\n")
                file.write("3. STRING REPLACEMENT ($v_(i) -> v[i])\n")
                file.write("=" * 80 + "\n")
                file.write(f"Original: {text}\n")
                file.write(f"Replaced: {replaced_text}\n")
                if v_matches:
                    file.write(f"Patterns found: {v_matches}\n")
                file.write("\n")

                # Words with vowels
                file.write("=" * 80 + "\n")
                file.write("4. WORDS STARTING OR ENDING WITH VOWELS\n")
                file.write("=" * 80 + "\n")
                file.write(f"Total words: {text_analysis['total_words']}\n")
                file.write(f"Words starting or ending with vowel: {text_analysis['vowel_words_count']}\n")
                if text_analysis['vowel_words']:
                    file.write(f"List: {', '.join(text_analysis['vowel_words'][:50])}\n")
                    if len(text_analysis['vowel_words']) > 50:
                        file.write(f"... and {len(text_analysis['vowel_words']) - 50} more\n")
                file.write("\n")

                # Character frequency
                file.write("=" * 80 + "\n")
                file.write("5. CHARACTER FREQUENCY\n")
                file.write("=" * 80 + "\n")
                freq = text_analysis['character_frequency']
                sorted_freq = sorted(freq.items())
                file.write("Character | Count\n")
                file.write("-" * 25 + "\n")
                for char, count in sorted_freq:
                    display_char = repr(char)[1:-1] if char in '\n\t\r ' else char
                    file.write(f"{display_char:^9} | {count}\n")
                file.write(f"\nTotal unique characters: {len(freq)}\n")
                file.write(f"Total characters: {sum(freq.values())}\n\n")

                file.write("=" * 80 + "\n")
                file.write("6. WORDS AFTER COMMA (Alphabetical Order)\n")
                file.write("=" * 80 + "\n")
                if text_analysis['words_after_comma']:
                    file.write(f"{', '.join(text_analysis['words_after_comma'])}\n")
                    file.write(f"\nTotal unique words: {len(text_analysis['words_after_comma'])}\n")
                else:
                    file.write("No words found after commas.\n")
                file.write("\n")

                file.write("=" * 80 + "\n")
                file.write("7. GENERAL TEXT STATISTICS\n")
                file.write("=" * 80 + "\n")
                file.write(f"Total sentences: {sentence_stats['total_sentences']}\n")
                file.write(f"Declarative sentences (повествовательные): {sentence_stats['declarative_count']}\n")
                file.write(f"Interrogative sentences (вопросительные): {sentence_stats['interrogative_count']}\n")
                file.write(f"Exclamatory sentences (побудительные): {sentence_stats['exclamatory_count']}\n")
                file.write(f"Average sentence length (word chars only): {sentence_stats['avg_sentence_length']:.2f}\n")
                file.write(f"Average word length: {sentence_stats['avg_word_length']:.2f}\n")
                file.write(f"Number of smileys: {sentence_stats['smiley_count']}\n")

                file.write("\n" + "=" * 80 + "\n")
                file.write("8. SENTENCES LIST\n")
                file.write("=" * 80 + "\n")
                for i, sentence in enumerate(sentence_stats['sentences_list'], 1):
                    sent_type = self._get_sentence_type_label(sentence)
                    file.write(f"{i}. [{sent_type}] {sentence}\n")

                file.write("\n" + "=" * 80 + "\n")
                file.write("END OF ANALYSIS\n")

            print(f"Results saved to {self.output_file}")
            return True

        except Exception as e:
            print(f"Error saving results: {e}")
            return False

    def _get_sentence_type_label(self, sentence: str) -> str:
        """Get sentence type label for display"""
        from .regex_patterns import RegexPatterns
        sent_type = RegexPatterns.classify_sentence(sentence)
        labels = {
            'declarative': 'повествовательное',
            'interrogative': 'вопросительное',
            'exclamatory': 'побудительное'
        }
        return labels.get(sent_type, 'повествовательное')

    def create_archive(self) -> bool:
        """
        Create zip archive of the results file

        Returns:
            True if successful, False otherwise
        """
        try:
            with zipfile.ZipFile(self.archive_name, 'w', zipfile.ZIP_DEFLATED) as archive:
                archive.write(self.output_file, os.path.basename(self.output_file))

            print(f"\nArchive created: {self.archive_name}")

            with zipfile.ZipFile(self.archive_name, 'r') as archive:
                print("\nArchive Information:")
                for info in archive.infolist():
                    print(f"   File: {info.filename}")
                    print(f"   Size: {info.file_size} bytes")
                    print(f"   Compressed: {info.compress_size} bytes")
                    if info.file_size > 0:
                        ratio = (1 - info.compress_size / info.file_size) * 100
                        print(f"   Compression ratio: {ratio:.1f}%")

            return True

        except Exception as e:
            print(f"Error creating archive: {e}")
            return False