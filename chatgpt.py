import os
from bs4 import BeautifulSoup

def process_html(input_file):
    # Extract the directory and filename from the input path
    directory, filename = os.path.split(input_file)

    with open(input_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all SVG tags in the HTML
    svg_tags = soup.find_all('svg')

    for svg_tag in svg_tags:
        # Check if the SVG tag has a 'fill' attribute
        if 'fill' in svg_tag.attrs:
            # Change the value of 'fill' to 'currentColor'
            svg_tag['fill'] = 'currentColor'

        # Find all path tags inside the SVG tag
        path_tags = svg_tag.find_all('path')

        for path_tag in path_tags:
            # Check if the path tag has a 'fill' attribute
            if 'fill' in path_tag.attrs:
                # Remove the 'fill' attribute from the path tag
                del path_tag['fill']

    # Create the output file path by joining the directory and filename
    output_file = os.path.join(directory, 'output_' + filename)

    # Write the modified HTML to the new file
    with open(output_file, 'w', encoding='utf-8') as new_file:  
        new_file.write(str(soup))

    return output_file

# Example usage
input_file_path = '/Users/dan/Downloads/Vector (4).svg'
output_file_path = process_html(input_file_path)
print(f"Output file saved at: {output_file_path}")
