#!/usr/bin/env python3

import os
from difflib import SequenceMatcher
from collections import defaultdict
from datetime import datetime

# Define the number of initial and final characters to consider for grouping files
PREFIX_LENGTH = 5
SUFFIX_LENGTH = 5
MIN_COMMON_SUBSTRING_LENGTH = 3

# List of common programming language extensions
COMMON_EXTENSIONS = {'.js', '.mjs', '.py', '.c', '.cpp', '.java', '.cs', '.sh', '.rb', '.php', '.html', '.css'}

# Function to find the longest common substring among a list of strings
def longest_common_substring(strs):
    substr = ''
    if len(strs) > 1 and len(strs[0]) > 0:
        seq_match = SequenceMatcher(None, strs[0], strs[1])
        match = seq_match.find_longest_match(0, len(strs[0]), 0, len(strs[1]))
        if match.size != 0:
            substr = strs[0][match.a: match.a + match.size].strip()
        for str in strs[2:]:
            seq_match.set_seq2(str)
            match = seq_match.find_longest_match(0, len(substr), 0, len(str))
            substr = substr[match.a: match.a + match.size]
    return substr

# Function to group and print files with similar prefixes or suffixes
def group_and_print_files(files):
    prefix_groups = defaultdict(list)
    suffix_groups = defaultdict(list)

    for file in files:
        prefix = file[:PREFIX_LENGTH]
        suffix = file[-SUFFIX_LENGTH:]
        prefix_groups[prefix].append(file)
        suffix_groups[suffix].append(file)

    all_groups = list(prefix_groups.values()) + list(suffix_groups.values())

    unique_groups = []
    for group in all_groups:
        if not any(set(group).issubset(set(other_group)) for other_group in all_groups if group != other_group):
            unique_groups.append(group)

    for group in unique_groups:
        if len(group) > 1:
            common_substring = longest_common_substring(group)
            if common_substring and len(common_substring) >= MIN_COMMON_SUBSTRING_LENGTH and not any(ext in common_substring for ext in COMMON_EXTENSIONS):
                print(f"\033[93m{common_substring}\033[0m")
                for file_name in group:
                    mod_time = os.path.getmtime(file_name)
                    print(f"{datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')} - {file_name}")

# List all .js and .mjs files in the current directory
files = [f for f in os.listdir('.') if (f.endswith('.js') or f.endswith('.mjs')) and os.path.isfile(f)]

# Group and print files with similar prefixes and suffixes
group_and_print_files(files)

