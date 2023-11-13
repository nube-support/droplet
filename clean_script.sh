#!/bin/bash

# Input and output file paths
input_file="output.txt"
output_file="cleaned_output.txt"

# Remove NUL characters and save the cleaned content to a new file
sed 's/␀//g' "$input_file" > "$output_file"

echo "Cleaned output saved to $output_file"
