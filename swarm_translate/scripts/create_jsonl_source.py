from typing import Dict, List
import json
import argparse
import os

# USFM to full book name mapping
USFM_TO_BOOK = {
    'GEN': 'Genesis',
    'EXO': 'Exodus',
    'LEV': 'Leviticus',
    'NUM': 'Numbers',
    'DEU': 'Deuteronomy',
    'JOS': 'Joshua',
    'JDG': 'Judges',
    'RUT': 'Ruth',
    '1SA': '1 Samuel',
    '2SA': '2 Samuel',
    '1KI': '1 Kings',
    '2KI': '2 Kings',
    '1CH': '1 Chronicles',
    '2CH': '2 Chronicles',
    'EZR': 'Ezra',
    'NEH': 'Nehemiah',
    'EST': 'Esther',
    'JOB': 'Job',
    'PSA': 'Psalms',
    'PRO': 'Proverbs',
    'ECC': 'Ecclesiastes',
    'SNG': 'Song of Solomon',
    'ISA': 'Isaiah',
    'JER': 'Jeremiah',
    'LAM': 'Lamentations',
    'EZK': 'Ezekiel',
    'DAN': 'Daniel',
    'HOS': 'Hosea',
    'JOL': 'Joel',
    'AMO': 'Amos',
    'OBA': 'Obadiah',
    'JON': 'Jonah',
    'MIC': 'Micah',
    'NAM': 'Nahum',
    'HAB': 'Habakkuk',
    'ZEP': 'Zephaniah',
    'HAG': 'Haggai',
    'ZEC': 'Zechariah',
    'MAL': 'Malachi',
    'MAT': 'Matthew',
    'MRK': 'Mark',
    'LUK': 'Luke',
    'JHN': 'John',
    'ACT': 'Acts',
    'ROM': 'Romans',
    '1CO': '1 Corinthians',
    '2CO': '2 Corinthians',
    'GAL': 'Galatians',
    'EPH': 'Ephesians',
    'PHP': 'Philippians',
    'COL': 'Colossians',
    '1TH': '1 Thessalonians',
    '2TH': '2 Thessalonians',
    '1TI': '1 Timothy',
    '2TI': '2 Timothy',
    'TIT': 'Titus',
    'PHM': 'Philemon',
    'HEB': 'Hebrews',
    'JAS': 'James',
    '1PE': '1 Peter',
    '2PE': '2 Peter',
    '1JN': '1 John',
    '2JN': '2 John',
    '3JN': '3 John',
    'JUD': 'Jude',
    'REV': 'Revelation'
}

def convert_usfm_reference(ref: str) -> str:
    """Convert a USFM reference (e.g., 'GEN 1:1') to full name format (e.g., 'Genesis 1:1')"""
    try:
        book_abbr, verse_ref = ref.strip().split(' ', 1)
        book_name = USFM_TO_BOOK.get(book_abbr.upper())
        if not book_name:
            raise ValueError(f"Unknown book abbreviation: {book_abbr}")
        return f"{book_name} {verse_ref}"
    except ValueError as e:
        print(f"Error processing reference: {ref}")
        raise e

def create_jsonl(id_file: str, content_file: str, output_file: str | None = None):
    """
    Create a JSONL file from separate id and content files.
    Will use contents until they run out, and filter out empty content entries.
    
    Args:
        id_file: Path to file containing USFM references
        content_file: Path to file containing content lines
        output_file: Path to output JSONL file. If None, uses content_file path with .jsonl extension
    """
    try:
        # Read both files
        with open(id_file, 'r', encoding='utf-8') as f:
            refs = [line.strip() for line in f if line.strip()]
        
        with open(content_file, 'r', encoding='utf-8') as f:
            contents = [line.strip() for line in f if line.strip()]
        
        # Log the file lengths
        print(f"Found {len(refs)} references and {len(contents)} content lines")
        
        # Default output file is input file with .jsonl extension
        if output_file is None:
            output_file = content_file.rsplit('.', 1)[0] + '.jsonl'
        
        # Create JSONL entries, only for non-empty content
        entries_written = 0
        with open(output_file, 'w', encoding='utf-8') as f:
            for ref, content in zip(refs, contents):  # zip will stop at shorter length
                if content:  # Only write entries with non-empty content
                    full_ref = convert_usfm_reference(ref)
                    entry = {
                        "id": full_ref,
                        "content": content
                    }
                    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                    entries_written += 1
        
        print(f"Successfully created {output_file} with {entries_written} entries")
        print(f"Skipped {len(contents) - entries_written} empty content entries")
        print(f"Note: {len(refs) - len(contents)} references were unused (likely deuterocanonical books)")
        
    except Exception as e:
        print(f"Error creating JSONL file: {str(e)}")
        raise e

def main():
    parser = argparse.ArgumentParser(description='Create JSONL file from separate id and content files')
    parser.add_argument('content_file', help='Path to file containing content lines')
    parser.add_argument('--output-file', help='Path to output JSONL file. Defaults to content file path with .jsonl extension')
    
    # Update the default path to be relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_vref_path = os.path.join(script_dir, '..', 'scenarios', 'data', 'vref.txt') # Assuming you run from swarm_translate directory
    
    parser.add_argument('--id-file', 
                       default=default_vref_path,
                       help='Path to file containing USFM references')
    
    args = parser.parse_args()
    create_jsonl(args.id_file, args.content_file, args.output_file)

if __name__ == "__main__":
    main()