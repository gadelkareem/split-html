#!env python3
# -*- coding: utf-8 -*-





import os
import argparse
from bs4 import BeautifulSoup, Tag
from collections import Counter

def split_html(input_file, output_dir='output', max_words=1800):
    # Make sure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open and parse the input HTML file
    with open(input_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Counter to keep track of the number of output files
    c = Counter()

    # List to hold links to all output files for the index
    output_files = []

    # Check for style and script tags and write to external files
    style_tag = soup.find('style')
    script_tag = soup.find('script')
    if style_tag:
        with open(f"{output_dir}/styles.css", 'w', encoding='utf-8') as f:
            f.write(style_tag.string)
        style_tag.decompose()
    if script_tag:
        with open(f"{output_dir}/script.js", 'w', encoding='utf-8') as f:
            f.write(script_tag.string)
        script_tag.decompose()

    # Iterate over the tags
    word_count = 0
    new_soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
    open_tags = []
    for content in soup.body.contents:
        if isinstance(content, Tag):
            word_count += len(str(content).split())
            open_tags.append(content.name)
        else:
            word_count += len(content.split())
        new_soup.body.append(content.extract())
        if word_count >= max_words:
            # Close any open tags
            for tag in reversed(open_tags):
                new_soup.body.append(BeautifulSoup(f'</{tag}>', 'html.parser'))

            # Generate the output filename
            c['files'] += 1
            output_file = f"{output_dir}/{output_dir}_{c['files']}.html"

            # Add style and script links to the head of the new soup object
            if style_tag:
                new_soup.head.append(soup.new_tag("link", rel="stylesheet", href="styles.css"))
            if script_tag:
                new_soup.body.append(soup.new_tag("script", src="script.js"))

            # Write the new soup object to the output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(new_soup))

            # Add a link to the output file to the list
            output_files.append(f"{output_dir}_{c['files']}.html")

            # Reset word_count and new_soup for the next chunk
            word_count = 0
            open_tags = []
            new_soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')

    # Create an index file with links to all output files
    with open(f"{output_dir}/{output_dir}_index.html", 'w', encoding='utf-8') as f:
        f.write("<html><body>\n")
        for file in output_files:
            f.write(f'<a href="{file}">{file}</a><br/>\n')
        f.write("</body></html>\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', help='The input HTML file to split', required=True)
    args = parser.parse_args()

    split_html(args.input_file)











