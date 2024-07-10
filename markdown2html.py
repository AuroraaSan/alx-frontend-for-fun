#!/usr/bin/python3
"""
This is a script to convert a Markdown file to HTML.

Usage:
    ./markdown2html.py README.md README.html

Arguments:
    input_file: the name of the Markdown file to be converted
    output_file: the name of the output HTML file

Example:
    ./markdown2html.py README.md README.html
"""

import pathlib
import re
import sys

def convert_md_to_html(input_file, output_file):
    """
    Converts markdown file to HTML file
    """
    # Read the contents of the input file
    with open(input_file, encoding='utf-8') as f:
        md_content = f.readlines()

    html_content = []
    in_list = False

    for line in md_content:
        # Check if the line is a heading
        heading_match = re.match(r'(#){1,6} (.*)', line)
        if heading_match:
            # Close list if currently in one
            if in_list:
                html_content.append('</ul>\n')
                in_list = False
            # Get the level of the heading
            h_level = len(heading_match.group(1))
            # Get the content of the heading
            h_content = heading_match.group(2)
            # Append the HTML equivalent of the heading
            html_content.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
        # Check if the line is a list item
        elif line.startswith('- '):
            if not in_list:
                html_content.append('<ul>\n')
                in_list = True
            item_content = line[2:].strip()
            html_content.append(f'<li>{item_content}</li>\n')
        else:
            # Close list if currently in one
            if in_list:
                html_content.append('</ul>\n')
                in_list = False
            html_content.append(line)

    # Close list if file ends with a list
    if in_list:
        html_content.append('</ul>\n')

    # Write the HTML content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(html_content)

if __name__ == '__main__':
    # Check if the number of arguments is less than 3
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the input file exists
    input_path = pathlib.Path(input_file)
    if not input_path.is_file():
        print(f'Missing {input_file}', file=sys.stderr)
        sys.exit(1)

    # Convert the markdown file to HTML
    convert_md_to_html(input_file, output_file)
