import requests
import telebot

# Your Telegram bot token
BOT_TOKEN = "6997982299:AAG72UFdN47fnjUDEASoQVrIzePL4ZlSeLA"

# CryptoCompare API details
CRYPTOCOMPARE_API_URL = "https://min-api.cryptocompare.com/data/histoday"
API_KEY = "72a7a3627d030f1b8f06ea07f5e30f32007d4e6e338ae584010feb82dab6f86e"

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    """Send a welcome message when the command /start is issued."""
    bot.reply_to(
        message, "Welcome to the Crypto Bot!\n\n"
        "Use /check <symbol1> <symbol2> ... to check if cryptocurrency symbols exist."
    )


@bot.message_handler(commands=['check'])
def check_symbol(message):
    """Check if the given cryptocurrency symbols exist."""
    try:
        # Extract symbols from the user's message
        symbols = message.text.split()[1:]

        if not symbols:
            bot.reply_to(
                message,
                "Please provide at least one symbol. Usage: /check <symbol1> <symbol2> ..."
            )
            return

        # Initialize lists for found and not found symbols
        found_symbols = []
        not_found_symbols = []

        for symbol in symbols:
            symbol = symbol.upper()
            # Check if the symbol exists using the API
            exists = check_symbol_exists(symbol)
            if exists:
                found_symbols.append(f" {symbol}")
            else:
                not_found_symbols.append(f" {symbol}")

        # Prepare the response message
        response_message = "Symbol check results:\n\n"

        # Add found symbols section
        if found_symbols:
            response_message += "**Found Symbols:**\n"
            response_message += "".join(found_symbols) + "\n"
        else:
            response_message += "\n**Found Symbols:**\nNo symbols found.\n\n"

        # Add not found symbols section
        if not_found_symbols:
            response_message += "**Not Found Symbols:**\n"
            response_message += "".join(not_found_symbols) + ""
        else:
            response_message += "\n**Not Found Symbols:**\nNo symbols not found.\n"

        bot.reply_to(message, response_message)

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")


def check_symbol_exists(symbol: str):
    """Check if a given symbol exists using the CryptoCompare API."""
    try:
        # Make a request to the CryptoCompare API
        params = {
            "fsym": symbol,
            "tsym": "USDT",
            "limit":
            1,  # Only fetch 1 day of data to check if the symbol exists
            "api_key": API_KEY,
            "e": "Bitget"
        }
        response = requests.get(CRYPTOCOMPARE_API_URL, params=params)
        data = response.json()

        # Check if the API returned valid data
        if data.get("Response") == "Error":
            return False  # Symbol not found
        else:
            return True  # Symbol found

    except Exception as e:
        print(f"Error checking symbol {symbol}: {e}")
        return False


if __name__ == "__main__":
    print("Bot started...")
    bot.infinity_polling()
