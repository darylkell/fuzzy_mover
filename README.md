# fuzzy_mover
Move target files to target location based on file name fuzzy matching to directory name. 
In other words, given the file name "Huffy the Brick Layer #38 (2023)", find a directory that closely matches this file name and move it there.

`filename` positional parameter supports home shortcut (~) and wildcard glob patterns.

```
usage: file_fuzzy.py [-h] [-o OUTPUT] [-y] [-t THRESHOLD] filename

Move files with glob patterns to the closest matching directory using fuzzy matching.

positional arguments:
  filename              The filename with optional glob patterns to be searched for.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        The directory to search through recursively for a matching directory. (Default: ./)
  -y, --yes             Automatically approve the move without confirmation.
  -t THRESHOLD, --threshold THRESHOLD
                        Threshold value to fuzzy match on (optional integer, default: 80)
```

### Installation
- Clone this repository
- Install requirements: `pip install -r requirements.txt`

### Example usage
Look for a directory in C:\Comics to move 'Huffy the Brick Layer' file into.<br>
```python file_fuzzy.py "Huffy the Brick Layer #38 (2023)" --output C:\Comics```

### Requirements
- fuzzywuzzy=0.18.0

### Security Warning
------
Please properly vet anything you download from the internet, including this script. It could do anything.
