import requests
import time


CRYPTO_API_KEY = '15351a21-8a86-45f4-9c82-c5d4d894eb1b'
TELEGRAM_BOT_TOKEN = '7806443764:AAGFG8r68Kg9TSGPLgjxCAGsT2ntnLEmZjg'
CHAT_ID = ' 2029136929'
CRYPTO_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

TARGET_PRICE = 20000
SYMBOL = 'bitcoin'
CURRENCY = 'USD'


def get_crypto_price(symbol, currency='USD'):
    headers = {
        'X-CMC_PRO_API_KEY': CRYPTO_API_KEY,
        'Accept': 'application/json'
    }
    params = {
        'symbol': symbol.upper(),  # Cryptocurrency symbol (Bitcoin, Ethereum, etc.)
        'convert': currency.upper()  # Convert to the specified currency (USD)
    }
    response = requests.get(CRYPTO_API_URL, headers=headers, params=params)
    
    # Print the full response for debugging purposes
    print("API Response:", response.json())  # Print the entire API response
    
    if response.status_code != 200:
        print(f"Error: Failed to fetch data. Status code: {response.status_code}")
        return None

    data = response.json()
    if data.get('status', {}).get('error_code') != 0:
        print(f"Error from API: {data.get('status', {}).get('error_message')}")
        return None

    # Extracting price
    try:
        price = data['data'][symbol.upper()]['quote'][currency.upper()]['price']
        return price
    except KeyError:
        print("Error: Cryptocurrency symbol or currency not found.")
        return None

# Function to send a message via Telegram
def send_telegram_message(message):
    telegram_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(telegram_url, data=payload)
    
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

# Main function to check the price and send an alert if the target price is reached
def check_price_and_alert():
    while True:
        price = get_crypto_price(SYMBOL, CURRENCY)
        
        if price is None:
            print(f"Failed to fetch price for {SYMBOL}")
        else:
            print(f"The current price of {SYMBOL} is ${price}")
            
            # Check if the price meets the target price criteria
            if price >= TARGET_PRICE:
                message = f"🚨 Alert! The price of {SYMBOL} is now ${price}, meeting or exceeding your target of ${TARGET_PRICE}."
                send_telegram_message(message)
                break  # Stop the loop after sending the alert

        # Wait for a specific interval before checking the price again (e.g., every 60 seconds)
        time.sleep(60)

# Run the bot
check_price_and_alert()
