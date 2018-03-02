# Author: Anupam Dagar
# GitHub: https://github.com/Anupam-dagar
# License: MIT License

import requests
from bs4 import BeautifulSoup
import json
import sys

global meta_data
meta_data = {}

# Download the source code of the website
def read_sourcecode( url ):
    try:
        source_code_response = requests.get(url)
        if source_code_response.status_code == 200:        
            return source_code_response.text
    except Exception:
        print("Unexpected error encountered. Please try again.")
        sys.exit(0)

# Extract facebook og meta data
def facebook_metadata(meta_tag):
    for tag in meta_tag:
        if tag.has_attr('property') and 'og:' in tag['property']:
            meta_data[tag['property']] = tag['content']

# Extract twitter meta data
def twitter_metadata(meta_tag):
    for tag in meta_tag:
        if tag.has_attr('name') and 'twitter:' in tag['name']:
            meta_data[tag['name']] = tag['content']

# Extract generic meta data
def generic_metadata(meta_tag):
    for tag in meta_tag:
        if tag.has_attr('name'):
            if 'description' in tag['name']:
                meta_data[tag['name']] = tag['content']
            if 'author' in tag['name']:
                meta_data[tag['name']] = tag['content']

# Driver function to run the script
def main():
    input_url = str(input("Enter website url:\n"))
    source_code = read_sourcecode(input_url)
    
    soup = BeautifulSoup(source_code, 'lxml')
    
    if soup.title is not None:
        meta_data['title'] = soup.title.text
    
    meta = soup.findAll('meta')
    
    generic_metadata(meta)
    facebook_metadata(meta)
    twitter_metadata(meta)
    
    # Write to json file
    with open('metadata.json', 'w') as metadatajson:
        json.dump(meta_data, metadatajson, indent=4)

    print("Meta data written to metadata.json")
    return meta_data

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Thanks for using meta-data-extractor.")
		sys.exit(0)