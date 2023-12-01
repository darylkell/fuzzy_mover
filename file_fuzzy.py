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
    return []

def parse_arguments():
    parser = argparse.ArgumentParser(description="Move files with glob patterns to the closest matching directory using fuzzy matching.")
    parser.add_argument("filename", help="The filename with optional glob patterns to be searched for.")
    parser.add_argument("-o", "--output", default="./", help="The directory to search through recursively for a matching directory. (Default: ./)")
    parser.add_argument("-y", "--yes", action="store_true", default=False, help="Automatically approve the move without confirmation.")
    parser.add_argument('-t', '--threshold', type=int, default=80, help='Threshold value to fuzzy match on (optional integer, default: 80)')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Use pathlib to handle paths and expand tilde character
    output_directory = Path(args.output).expanduser()

    # Use pathlib to expand wildcard patterns and expand tilde character
    input_files = list(Path(args.filename).expanduser().resolve().parent.glob(Path(args.filename).name))

    if not input_files:
        print(f"Error: No files found matching name '{args.filename}'.")
        return    
    
    available_directories = {d: d.name for d in output_directory.rglob("*") if d.is_dir()}
    for i, input_file in enumerate(input_files, start=1):
        print(f"\n{i}/{len(input_files)} Processing file : '{input_file.name}'")
        
        target_directory = input_file.stem
        matches = find_closest_directories(target_directory, available_directories, args.threshold)
        if not matches: 
            print(f"No match found for '{target_directory}'.")
            continue

        for match, score in matches:
            destination_directory = output_directory / match

            # Offer the match to the user
            print(f"Match: {destination_directory}   (Score: {score})")
            if not args.yes:
                move_or_skip = input("Do you want to move the file? (Y/n/skip): ").lower()
                if move_or_skip in ("skip", "s"):
                    break
            if args.yes or move_or_skip != "n":
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
