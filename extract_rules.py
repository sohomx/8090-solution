import re
import os

def extract_rules_from_file(filepath, outfile):
    print(f"Processing {filepath}...")  # Debug print
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, 'r') as f:
        lines = f.readlines()
    pattern = re.compile(r'(\$\d+(\.\d{2})?)|mile|per diem|cap|capped|exception|limit|bonus|if|unless|except|over|minimum|maximum|receipt|day|weekend|penalty|override', re.I)
    matches = 0
    with open(outfile, 'a') as out:
        for i, line in enumerate(lines):
            if pattern.search(line):
                out.write(f"{filepath}:{i+1}: {line.strip()}\n")
                matches += 1
    print(f"Wrote {matches} matches from {filepath} to {outfile}")

# Clear file first
open('raw_rules_candidates.txt', 'w').close()

# Run for both files
extract_rules_from_file('PRD.md', 'raw_rules_candidates.txt')
extract_rules_from_file('INTERVIEWS.md', 'raw_rules_candidates.txt')