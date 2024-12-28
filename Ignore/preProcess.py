import os
from bs4 import BeautifulSoup

# Step 1: Locate the first available HTML file in the current directory
html_files = [file for file in os.listdir('.') if file.endswith('.html')]
if not html_files:
    print("No HTML files found in the current directory.")
    exit()

html_file = html_files[0]

# Step 2: Parse the HTML file and find divs with the specified ID
with open(html_file, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')


div_elements = soup.find_all('div', attrs={"data-rbd-draggable-context-id": True})


# Ignore the last one in the list
if div_elements:
    div_elements = div_elements[:-1]


# Step 3: Extract locations from the div elements
locations = []
for div in div_elements:
    button = div.find('button', class_="ListViewItem__placeName")
    if button:
        span = button.find('span', class_="text-wrap overflow-hidden")
        if span:
            locations.append(span.text.strip())

# Output the list of locations
#print("Locations:", locations)

#Save the locations to a file called raw_locations.csv
with open('raw_locations.csv', 'w', encoding='utf-8') as file:
    for location in locations:
        file.write(location + '\n')



