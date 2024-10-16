def remove_duplicates(input_file, output_file):
    # Create an empty set to store unique wallet addresses
    unique_wallets = set()

    # Read the existing file and collect unique wallet addresses
    with open(input_file, 'r') as infile:
        for line in infile:
            address = line.strip()  # Strip leading/trailing whitespace
            if address:  # Ignore empty lines
                unique_wallets.add(address)

    # Write the unique addresses to the new file
    with open(output_file, 'w') as outfile:
        for wallet in sorted(unique_wallets):  # Optional: Sort the addresses if needed
            outfile.write(wallet + '\n')

    print(f"Unique wallet addresses have been written to {output_file}")

# File paths
input_file = 'bitcoin_addresses.txt'
output_file = 'BitcoinFog.txt'

# Run the function to remove duplicates
remove_duplicates(input_file, output_file)
