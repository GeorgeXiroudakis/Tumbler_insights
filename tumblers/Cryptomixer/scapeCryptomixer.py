import requests
from bs4 import BeautifulSoup
import time

# Define the URL you want to scrape
url = 'https://bitcoinmixer1.com/request/sdfsd$100$0$1.235'
# Define the file path where you want to append the wallet addresses
file_path = 'Cryptomixer'

def get_mixing_address():
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the input element with the desired class
        input_element = soup.find('input', {'class': 'form-control fsb-md-4 mixaddr'})

        if input_element:
            # Extract the value attribute
            mixing_address = input_element['value']
            print(f"Mixing Address: {mixing_address}")

            # Append the address to the file
            with open(file_path, 'a') as outfile:
                outfile.write(mixing_address + '\n')  # Append address with a newline
        else:
            print("Input element not found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Run the scraper in a loop
try:
    while True:
        get_mixing_address()
        time.sleep(5)  # Refresh every 5 seconds (adjust as needed)
except KeyboardInterrupt:
    print("Scraper stopped.")
