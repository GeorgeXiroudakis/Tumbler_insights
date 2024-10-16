import requests
import re
import time

# Set the base URL and output file
base_url = "https://www.walletexplorer.com/wallet/HelixMixer{}/addresses?page={}"
output_file = "HelixMixerOG.txt"

# Define the regex pattern for Bitcoin addresses
pattern = r'\b(bc(0([ac-hj-np-z02-9]{39}|[ac-hj-np-z02-9]{59})|1[ac-hj-np-z02-9]{8,87})|[13][a-km-zA-HJ-NP-Z1-9]{25,35})\b'

# Define suffixes and corresponding page ranges
folders = {
    "": 15,  # No suffix, 62 pages
    "-old": 25,  # For example, -old has 25 pages
    "-old2": 89,  # Another example, -old2 has 30 pages
    "-old3": 62,
    "-old4": 97,
    "-old5": 34,
    "-old6": 61,
    "-old7": 64,
    "-old8": 29,
    "-old9": 84,
    "-old10": 77,
    "-old11": 19,
    "-old12": 81,
    "-old13": 61,
    "-old14": 88,
    "-old15": 80,
    "-old16": 104,
    "-old17": 85,
    "-old18": 122,
    "-old19": 93,
    "-old20": 88,
    "-old21": 74,
    "-old22": 55,
    "-old23": 72,
    "-old24": 63,
    "-old25": 71,
    "-old26": 52,
    "-old27": 103,
    "-old28": 95,
    "-old29": 51,
    "-old30": 69,
    "-old31": 53,
    "-old32": 40,
    "-old33": 107,
    "-old34": 109
}

# Create or clear the output file (comment this if appending to an existing file)
with open(output_file, 'w') as f:
     f.write("")

# Loop through each folder and its corresponding number of pages
for suffix, total_pages in folders.items():
    for page in range(1, total_pages + 1):
        url = base_url.format(suffix, page)
        print(f"Fetching page {page} for folder '{suffix}': {url}")

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
                print(f"Error fetching page {page} for folder '{suffix}': {e}")

print("Done fetching addresses.")
