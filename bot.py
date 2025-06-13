import telebot
from telebot import types

# Your BotFather Token
BOT_TOKEN = "7562603920:AAFciDZ9N33KjgtNr4fI8Xr-NmXIfCOCKoM"

bot = telebot.TeleBot(BOT_TOKEN)

products = {
    "CP": {"price": 10, "link": "https://t.me/+6yP9JK3YfwRlN2Qx"},
    "Force": {"price": 10, "link": "https://t.me/+6yP9JK3YfwRlN2Qx"},
    "Teen": {"price": 10, "link": "https://t.me/+6yP9JK3YfwRlN2Qx"},
    "Unlock All": {"price": 25, "link": "https://t.me/+6yP9JK3YfwRlN2Qx"}
}

wallets = {
    "BTC": "1842quq6reE5UQbojfUFJJCYWzEviSss5k",
    "USDT(TRC20)": "TLuLwvgWU7jS9bmHesZzZnhZjRqMN5cgAm",
    "LTC": "LSBtFhxdR8XnKmCmpjwynTCnRxmHhTNYve",
    "USDC(Polygon)": "0x375f0c9ca8747b3b50bfae467dd37431c1a04368",
    "ETH(ERC20)": "0x375f0c9ca8747b3b50bfae467dd37431c1a04368"
}

user_selections = {}

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for product in products:
        markup.add(product)
    bot.send_message(message.chat.id, "Welcome! Please select which package you want:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in products.keys())
def product_selected(message):
    user_selections[message.chat.id] = {"product": message.text}
    product = products[message.text]
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for coin in wallets:
        markup.add(coin)
    bot.send_message(message.chat.id,
                     f"You selected *{message.text}* for *${product['price']}*.\n"
                     f"Please select your crypto to pay:",
                     reply_markup=markup,
                     parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text in wallets.keys())
def coin_selected(message):
    selection = user_selections.get(message.chat.id)
    if not selection or "product" not in selection:
        bot.send_message(message.chat.id, "Please select a package first by typing /start.")
        return
    selection["coin"] = message.text
    coin = message.text
    wallet = wallets[coin]
    price = products[selection["product"]]["price"]
    bot.send_message(message.chat.id,
                     f"Send *${price}* worth of *{coin}* to this address:\n\n`{wallet}`\n\n"
                     f"After payment, send /paid and wait for confirmation.",
                     parse_mode="Markdown")

@bot.message_handler(commands=["paid"])
def payment_notice(message):
    if message.chat.id not in user_selections or "product" not in user_selections[message.chat.id]:
        bot.send_message(message.chat.id, "You need to select a package and coin first. Use /start.")
        return
    bot.send_message(message.chat.id,
                     "Thanks for the payment notification! Please wait for manual confirmation.")

@bot.message_handler(commands=["confirm"])
def confirm(message):
    admin_id = 8137676833  # Your Telegram ID
    if message.from_user.id != admin_id:
        bot.send_message(message.chat.id, "You are not authorized to confirm payments.")
        return
    try:
        parts = message.text.split()
        user_id = int(parts[1])
    except:
        bot.send_message(message.chat.id, "Usage: /confirm <user_id>")
        return
    if user_id not in user_selections:
        bot.send_message(message.chat.id, "User ID not found.")
        return
    product = user_selections[user_id]["product"]
    link = products[product]["link"]
    bot.send_message(user_id, f"🎉 Payment confirmed! Here is your unlock link:\n{link}")
    bot.send_message(message.chat.id, f"User {user_id} confirmed for {product}.")
    user_selections.pop(user_id, None)

@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, "Use /start to select package and pay.\nAdmins use /confirm <user_id> to confirm payment.\nAfter payment, user sends /paid to notify.")

bot.infinity_polling()
