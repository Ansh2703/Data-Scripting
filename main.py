from bs4 import BeautifulSoup
import requests
import sys
from tabulate import tabulate

# URL of the webpage containing the table
url = "https://en.wikipedia.org/wiki/Big_Tech_(India)"

# Fetch the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Set the output encoding to UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Function to extract table data
    def extract_table(table):
        headers = [th.text.strip() for th in table.find_all('th')]
        rows = []
        for tr in table.find_all('tr'):
            cells = tr.find_all(['td', 'th'])
            row = [cell.text.strip() for cell in cells]
            rows.append(row)
        return headers, rows
    
    # Find all tables with the class 'wikitable'
    tables = soup.find_all('table', {'class': 'wikitable'})
    
    if tables:
        for index, table in enumerate(tables):
            headers, rows = extract_table(table)
            print(f"Table {index + 1}")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            print("\n")
    else:
        print("Table not found.")
    
    # Extract summary or introduction paragraph
    summary = soup.find('div', {'class': 'mw-parser-output'}).find('p').text.strip()
    print("Summary:")
    print(summary)
    print("\n")
    
    # Extract infobox if present
    infobox = soup.find('table', {'class': 'infobox'})
    if infobox:
        headers, rows = extract_table(infobox)
        print("Infobox:")
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("Infobox not found.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
