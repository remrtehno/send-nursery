import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin  # Import urljoin function

import json


# Define the URL of the webpage you want to scrape
base_url  = 'https://nabor.pcss.pl/warszawa/zlobek/oferta'  # Replace with the actual URL

# Send an HTTP GET request to the base URL
response = requests.get(base_url)

# Create a dictionary to store email addresses and their corresponding links
email_data = {}

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the base page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags matching the selector
    links = soup.select("#unitstable tr td")

    # Loop through each link
    # Loop through each link
    for link in links:
        # Check if the 'href' attribute exists for the link
        if link:
            # Get the href attribute of the link
            link_url = link.find('a', href=True)

    
            if link_url:
                link_url = link_url['href']
            else:
                link_url = ""

            print(link_url)
       

            # Construct the absolute URL using urljoin
            absolute_url = urljoin(base_url, link_url)

            # Load the content of the linked page
            linked_response = requests.get(absolute_url)

            # Check if the request for the linked page was successful
            if linked_response.status_code == 200:
                # Parse the content of the linked page
                linked_soup = BeautifulSoup(linked_response.text, 'html.parser')

                # Use regular expressions to find email addresses in the linked page content
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                emails = re.findall(email_pattern, linked_soup.get_text())

                # Print the collected email addresses
                if emails:
                    print("Emails found on", absolute_url)
                    email_data[absolute_url] = emails[0]
                    print(emails[0])
            else:
                print('Failed to retrieve the linked page:', absolute_url)
        else:
            print('No href attribute found for the link')
else:
    print('Failed to retrieve the base webpage. Status code:', response.status_code)

# Save the email data to a JSON file
with open('email_data.json', 'w') as json_file:
    json.dump(email_data, json_file, indent=4)

# #unitstable tr td a:first-child