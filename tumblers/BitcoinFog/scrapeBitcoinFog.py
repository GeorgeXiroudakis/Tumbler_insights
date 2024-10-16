import requests
import re
import time

# Set the base URL and output file
base_url = "https://www.walletexplorer.com/wallet/BitcoinFog/addresses?page={}"
output_file = "bitcoin_addresses.txt"

# Define the regex pattern for Bitcoin addresses
pattern = r'\b(bc(0([ac-hj-np-z02-9]{39}|[ac-hj-np-z02-9]{59})|1[ac-hj-np-z02-9]{8,87})|[13][a-km-zA-HJ-NP-Z1-9]{25,35})\b'

# Create or clear the output file
with open(output_file, 'w') as f:
    f.write("")

# Loop through pages 1 to 2450
for page in range(1, 2451):
    url = base_url.format(page)
    print(f"Fetching page {page}: {url}")

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Apply the regex to extract Bitcoin addresses
        addresses = re.findall(pattern, response.text)

        # Write the found addresses to the output file
        with open(output_file, 'a') as f:
            for address in addresses:
                # address[0] contains the matched address
                f.write(address[0] + "\n")

        # Wait for a short time before the next request
        time.sleep(2)  # Delay for 2 seconds

    except requests.exceptions.HTTPError as e:
        # Handle specific HTTP errors
        if response.status_code == 429:
            print(f"Rate limit exceeded. Waiting for 60 seconds before retrying...")
            time.sleep(60)  # Wait longer if rate limit is hit
        else:
            print(f"Error fetching page {page}: {e}")

print("Done fetching addresses.")
