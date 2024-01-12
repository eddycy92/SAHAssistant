#!/usr/bin/env python3
import sys
import re
import os

def remove_comments(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    code_without_comments = ""
    comment_pattern = r"^\s*#.*"

    for line in lines:
        if not re.match(comment_pattern, line):
            code_without_comments += line

    return code_without_comments

def main():
    if len(sys.argv) != 2:
        print("Usage: nocom <file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = input_file_path + ".txt"
    
    code = remove_comments(input_file_path)
    with open(output_file_path, 'w') as output_file:
        output_file.write(code)
    
    print(f"Code without comments saved to {output_file_path}")

if __name__ == "__main__":
    main()