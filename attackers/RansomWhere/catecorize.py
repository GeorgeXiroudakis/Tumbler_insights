import json
import os
import re
from collections import defaultdict

# Specify the path to your JSON file
file_path = 'data.json'

# Directory to save the JSON files
output_directory = 'strands'

# Create the 'strands' directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Open the file and load its contents
with open(file_path, 'r') as file:
    data = json.load(file)


# Function to sanitize filenames
def sanitize_filename(name):
    return re.sub(r'[\/:*?"<>|]', '_', name)  # Replace invalid characters with '_'


# Group items by 'family'
family_groups = defaultdict(list)

for item in data:
    family = item.get('family', 'unknown')  # Use 'unknown' if 'family' field is missing
    family_groups[family].append(item)

# Write each family group to a separate JSON file in the 'strands' directory
for family, items in family_groups.items():
    # Sanitize the family name to create a valid filename
    sanitized_family = sanitize_filename(family)
    filename = os.path.join(output_directory, f'{sanitized_family}.json')

    with open(filename, 'w') as outfile:
        json.dump(items, outfile, indent=4)
    print(f"Created {filename} with {len(items)} items")
