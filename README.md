# Split HTML

## Description
Split HTML is a simple python script that splits a HTML file into multiple files based on the max number of words per file. This is useful for creating multiple HTML files for ChatGPT to read from. It can also create markdown files form the HTML file.

## Usage
```
# Split into HTML
python3 split-html.py -i <html_file> -o <output_dir> -u <url_root>
# Split into Markdown
python3 split-md.py -i <html_file> -o <output_dir> -u <url_root>
```

## Arguments
```
-i, --input_file: The HTML file to split
-o, --output_dir: The output directory to save the split files
-u, --url_root: The root URL to use to prefix the paths
```

## Requirements
- Python 3.6+
- BeautifulSoup4
- html2text
```
python3 -m pip install -r requirements.txt
```

