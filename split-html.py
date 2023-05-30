#!env python3
# -*- coding: utf-8 -*-


import os
import argparse
import bs4
from collections import Counter
from urllib.parse import urljoin


def split_html(input_file, output_dir, url_root, max_words=1800):
    # Make sure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open and parse the input HTML file
    with open(input_file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')

    # Counter to keep track of the number of output files
    c = Counter()

    # List to hold links to all output files for the index
    output_files = []

    # Variables to hold the current chunk of elements and the current word count
    chunk = []
    word_count = 0

    # Update image src attributes with url_root
    for img in soup.find_all('img'):
        img['src'] = urljoin(urljoin(url_root, output_dir) + '/', img['src'])

    # Iterate over the elements in the HTML body
    for element in soup.body:
        # Split the string representation of the element into words
        words = str(element).split()

        # Check if adding the words from this element would exceed the maximum word count
        if word_count + len(words) > max_words:
            # If so, write the current chunk of elements to an output file
            c['files'] += 1
            output_file = f"{output_dir}/{output_dir}_{c['files']}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                for e in chunk:
                    f.write(str(e))
            output_files.append(output_file)

            # Start a new chunk with the current element
            chunk = [element]
            word_count = len(words)
        else:
            # If not, add the current element to the chunk
            chunk.append(element)
            word_count += len(words)

    # Write any remaining elements to a final output file
    if chunk:
        c['files'] += 1
        output_file = f"{output_dir}/{output_dir}_{c['files']}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            for e in chunk:
                f.write(str(e))
        output_files.append(output_file)

    # Create an index file with links to all output files
    with open(f"{output_dir}/{output_dir}_index.html", 'w', encoding='utf-8') as f:
        for file in output_files:
            # Create a URL for the file based on the URL root directory
            file_url = os.path.join(url_root, file)
            f.write(f'<a href="{file_url}">{file_url}</a><br>\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', help='The input HTML file to split', required=True)
    parser.add_argument('-o', '--output_dir', help='The output directory for the split HTML files', required=False,
                        default='output')
    parser.add_argument('-u', '--url_root', help='The root directory URL on the server', required=False, default='/')
    args = parser.parse_args()

    split_html(args.input_file, args.output_dir, args.url_root)
