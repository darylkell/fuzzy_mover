from pathlib import Path
from fuzzywuzzy import process # pip install fuzzywuzzy
from fuzzywuzzy import fuzz
import argparse

from collections import Counter

def find_closest_directories(target_directory: str, available_directories: dict[str, str], threshold=80):
    # Use fuzzy matching to find the closest match
    # You can set a threshold for the matching score based on your requirements   
    threshold = 0
    matches = process.extract(target_directory, available_directories.values())
    matches_above_threshold = [(match, score) for match, score in matches if score >= threshold]

    available_directories_containing_matches = []
    for match, score in matches_above_threshold:
        for dir in available_directories.keys():
            if match in str(dir) and (dir, score) not in available_directories_containing_matches:
                available_directories_containing_matches.append((dir, score))

    if available_directories_containing_matches:
        return available_directories_containing_matches
    print(f"No close match found for '{target_directory}'.")
    exit(1)


def confirm_move():
    user_input = input("Do you want to move the file? (Y/n): ").lower()
    return user_input != 'n'

def parse_arguments():
    parser = argparse.ArgumentParser(description="Move downloaded files with glob patterns to the closest matching directories using fuzzy matching.")
    parser.add_argument("filename", help="The filename with optional glob patterns to be searched for.")
    parser.add_argument("-o", "--output", help="The directory to search through recursively for a matching directory.")
    parser.add_argument("-y", "--yes", action="store_true", help="Automatically approve the move without confirmation.")

    return parser.parse_args()

def main():
    args = parse_arguments()

    # Use pathlib to handle paths and expand tilde character
    download_directory = Path(args.output).expanduser() if args.output else Path.cwd()

    # Use pathlib to expand wildcard patterns and expand tilde character
    input_files = list(Path(args.filename).expanduser().resolve().parent.glob(Path(args.filename).name))

    if not input_files:
        print(f"Error: No files found matching the pattern '{args.filename}'.")
        return    
    
    for i, input_file in enumerate(input_files, start=1):
        # Find the closest matching directory
        target_directory = input_file.stem
        available_directories = {d: d.name for d in download_directory.rglob("*") if d.is_dir()}
        matches = find_closest_directories(target_directory, available_directories)

        print(f"\nProcessing file {i}/{len(input_files)}: '{input_file.name}'")

        for match, score in matches:
            destination_directory = download_directory / match

            # Offer the match to the user
            print(f"Match: {destination_directory} (Score: {score})")
            if args.yes or confirm_move():
                final_path = destination_directory / input_file.name
                if not final_path.exists() or input("That file exists, overwrite? (Y/n)") != "n":
                    final_path.write_bytes(input_file.read_bytes())  # gets around moving to network location on windows
                    input_file.unlink()
                    print(f"File moved to: {destination_directory}")
                break
        else:
            print("No more matches above the threshold.")


if __name__ == "__main__":
    main()
