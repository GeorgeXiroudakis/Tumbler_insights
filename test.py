import requests
from stem import Signal
from stem.control import Controller
import time

# Function to change Tor IP
def change_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='xiroudakis')  # Authenticate using the password if set
        controller.signal(Signal.NEWNYM)  # Request a new identity
        print("New Tor IP address requested.")

# Function to get transaction details from BlockCypher via Tor
def get_transaction_details(tx_hash):
    url = f"https://api.blockcypher.com/v1/btc/main/txs/{tx_hash}"
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

    try:
        response = session.get(url)
        if response.status_code == 200:
            tx_data = response.json()
            return tx_data
        elif response.status_code == 429:  # Rate limit exceeded
            print("Error: Rate limit exceeded. Trying again with a new Tor IP...")
            change_tor_ip()  # Change IP
            return get_transaction_details(tx_hash)  # Retry after IP change
        else:
            print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to parse and print transaction details
def print_transaction_details(tx_data):
    if tx_data:
        print("Transaction Hash:", tx_data.get('hash'))

        # Print input addresses
        print("\nInputs (where the funds came from):")
        for inp in tx_data.get('inputs', []):
            addresses = inp.get('addresses', [])
            amount = inp.get('output_value', 0) / 1e8  # Convert from satoshi to BTC
            print(f" - Address: {addresses}, Amount: {amount} BTC")

        # Print output addresses
        print("\nOutputs (where the funds went):")
        for out in tx_data.get('outputs', []):
            addresses = out.get('addresses', [])
            amount = out.get('value', 0) / 1e8  # Convert from satoshi to BTC
            print(f" - Address: {addresses}, Amount: {amount} BTC")
    else:
        print("No transaction data available.")

# Example usage
if __name__ == "__main__":
    while True:
        # Replace with your own transaction hash
        transaction_hash = "cfb39d98f66da8bfe42ad86894f116a3c1d8c6d1189456fcffae615a80623c49"

        # Fetch transaction details
        transaction_data = get_transaction_details(transaction_hash)

        # Print transaction details
        print_transaction_details(transaction_data)

