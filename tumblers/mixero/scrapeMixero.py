from playwright.sync_api import sync_playwright
import time

# Define the wallet address
wallet_address = 'bc1quw2p687tj0g04eyrftemtasc5s4vtawakta6pt'
file_path = 'mixero.txt'  # Path to the output file

def automate_mixero():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)  # Set to True for headless mode
        page = browser.new_page()

        # Continuously run the process
        try:
            while True:
                # Navigate to the URL
                page.goto('https://mixero.io/mix_coinjoin')

                # Wait for the destination address input to be available and fill it
                page.wait_for_selector('#destination_address-1')
                page.fill('#destination_address-1', wallet_address)

                page.wait_for_timeout(1000);

                # Click the checkbox
                page.click('.checkmark')

                page.wait_for_timeout(1000);

                # Click the 'Proceed' button
                page.click('#cbcoin-submit')

                # Wait for the next page to load and the bitcoin address to appear
                page.wait_for_selector('#bitcoin-address-input')

                # Extract the value of the bitcoin address
                bitcoin_address = page.get_attribute('#bitcoin-address-input', 'value')
                print(f'Bitcoin Address: {bitcoin_address}')

                # Append the bitcoin address to the file
                with open(file_path, 'a') as file:
                    file.write(bitcoin_address + '\n')

                # Wait for a few seconds before repeating (adjust the sleep time as necessary)
                time.sleep(5)

        except KeyboardInterrupt:
            # Graceful exit when Ctrl+C is pressed
            print("Scraping stopped by user.")

        finally:
            # Close the browser when the loop terminates
            browser.close()

# Run the function
automate_mixero()
