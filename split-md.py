#!env python3
# -*- coding: utf-8 -*-
import os
import re
import argparse
import html2text
from collections import Counter
from urllib.parse import urljoin


def split_markdown(input_file, output_dir='output', url_root='', max_words=1800):
    # Make sure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open and parse the input HTML file
    with open(input_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Convert HTML to Markdown
    h = html2text.HTML2Text()
    h.body_width = 0
    markdown = h.handle(html)

    # Add the url_root to image paths in Markdown
    markdown = re.sub(r'\[(.*?)\]\((.*?)\)', lambda
        match: f"[{match.group(1)}]({urljoin(urljoin(url_root, output_dir) + '/', match.group(2))})", markdown)

    # Write the Markdown to a file
    with open(f"{output_dir}/{output_dir}.md", 'w', encoding='utf-8') as f:
        f.write(markdown)

    # Counter to keep track of the number of output files
    c = Counter()

    # List to hold links to all output files for the index
    output_files = []

    # Variables to hold the current chunk of words and the current word count
    chunk = []
    word_count = 0

    # Iterate over the lines of the Markdown
    for line in markdown.split('\n'):
        # Split the line into words
        words = line.split()
        words.append('\n')

        # Check if adding the words from this line would exceed the maximum word count
        if word_count + len(words) > int(max_words):
            # If so, write the current chunk of words to an output file
            c['files'] += 1
            output_file = f"{output_dir}/{output_dir}_{c['files']}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(' '.join(chunk))
            output_files.append((output_file, f"{output_dir}_{c['files']}.md"))

            # Start a new chunk with the words from this line
            chunk = words
            word_count = len(words)
        else:
            # If not, add the words from this line to the current chunk
            chunk += words
            word_count += len(words)

    # Write any remaining words to a final output file
    if chunk:
        c['files'] += 1
        output_file = f"{output_dir}/{output_dir}_{c['files']}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(' '.join(chunk))
        output_files.append((output_file, f"{output_dir}_{c['files']}.md"))

    # Create an index file with links to all output files
    with open(f"{output_dir}/{output_dir}_index.md", 'w', encoding='utf-8') as f:
        for file, text in output_files:
            file_url = urljoin(url_root, file)
            f.write(f'{file_url}\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', help='The input HTML file to split', required=True)
    parser.add_argument('-o', '--output_dir', help='The output directory name', required=False, default='output')
    parser.add_argument('-u', '--url_root', help='The root directory URL on the server', required=False, default='')
    parser.add_argument('-w', '--max_words', help='The maximum number of words per output file', required=False,
                        default=1800)
    args = parser.parse_args()

    split_markdown(args.input_file, args.output_dir, args.url_root, args.max_words)
