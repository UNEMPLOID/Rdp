import telebot
from telebot import types
import logging
import time

# Enable logging
logging.basicConfig(level=logging.INFO)

# Bot token and log group ID
TOKEN = '7358780729:AAHF1wFekVfEBwYUd4i9uX5JWl3EFVUWxfM'
LOG_GROUP_ID = -1002155266073

# Channels and group
REQUIRED_CHANNELS = ["@Found_Us", "@Falcon_security", "@Pbail_Squad"]
REQUIRED_GROUP = "@indian_hacker_group"
OWNER = "Moon_God_Khonsu"

# List to store user details
user_data = {}

# Initialize bot
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username

    if user_id not in user_data:
        user_data[user_id] = user_name

    # Inline buttons
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("Found Us", url="https://t.me/Found_Us"),
        types.InlineKeyboardButton("Falcon Security", url="https://t.me/Falcon_security")
    )
    keyboard.add(
        types.InlineKeyboardButton("Indian Hacker Group", url="https://t.me/indian_hacker_group"),
        types.InlineKeyboardButton("PBAIL COMM", url="https://t.me/Pbail_Squad")
    )
    keyboard.add(
        types.InlineKeyboardButton("Verify", callback_data='verify')
    )
    keyboard.add(
        types.InlineKeyboardButton("Owner", url="https://t.me/Moon_God_Khonsu")
    )

    # Welcome message
    welcome_message = "Welcome! Please join all the required channels and group to use the bot."
    try:
        bot.send_photo(message.chat.id, "https://i.ibb.co/Jcf4gyy/20240126-165040-0000.png", caption=welcome_message, reply_markup=keyboard)
    except telebot.apihelper.ApiTelegramException as e:
        logging.error(f"Failed to send welcome message to user {user_id}: {e}")
        bot.send_message(
            chat_id=LOG_GROUP_ID,
            text=f"Failed to send welcome message to user {user_id}: {e}"
        )

    # Logging new user start
    try:
        bot.send_message(
            chat_id=LOG_GROUP_ID,
            text=f"➕ New User Notification ➕\n\n👤 User: @{user_name}\n🆔 User ID: {user_id}\n🌝 Total Users Count: {len(user_data)}"
        )
    except telebot.apihelper.ApiTelegramException as e:
        logging.error(f"Failed to log new user start for user {user_id}: {e}")

@bot.callback_query_handler(func=lambda call: call.data == 'verify')
def process_callback_verify(call: telebot.types.CallbackQuery):
    user_id = call.from_user.id
    user_name = call.from_user.username

    # Verification check
    try:
        is_verified = all([bot.get_chat_member(channel, user_id).status in ['member', 'administrator', 'creator'] for channel in REQUIRED_CHANNELS])
        is_verified &= bot.get_chat_member(REQUIRED_GROUP, user_id).status in ['member', 'administrator', 'creator']
    except telebot.apihelper.ApiTelegramException as e:
        logging.error(f"Verification check failed for user {user_id}: {e}")
        bot.send_message(
            chat_id=user_id,
            text="Error during verification. Please try again later."
        )
        return
    
    if is_verified:
        # If user is verified
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("Free RDP", web_app=types.WebAppInfo(url="https://app.apponfly.com/trial"))
        )
        try:
            bot.send_message(
                chat_id=user_id,
                text="Thank you for using our service. Press the Free RDP button to use RDP.",
                reply_markup=keyboard
            )
        except telebot.apihelper.ApiTelegramException as e:
            logging.error(f"Failed to send Free RDP message to user {user_id}: {e}")
    else:
        # If user is not verified
        try:
            bot.send_message(
                chat_id=user_id,
                text="Please join all the required channels and group first to use the bot."
            )
        except telebot.apihelper.ApiTelegramException as e:
            logging.error(f"Failed to send verification failure message to user {user_id}: {e}")

@bot.callback_query_handler(func=lambda call: call.data == 'commands')
def send_commands(call: telebot.types.CallbackQuery):
    commands = (
        "/start - Start the bot\n"
        "/broadcast <message> - Broadcast a message to all users\n"
        "/stats - Get statistics about the bot\n"
    )
    try:
        bot.send_message(call.message.chat.id, "Here are the bot commands:\n" + commands)
    except telebot.apihelper.ApiTelegramException as e:
        logging.error(f"Failed to send commands to user {call.from_user.id}: {e}")

@bot.message_handler(commands=['broadcast'])
def broadcast(message: telebot.types.Message):
    if message.from_user.username == OWNER[1:]:
        message_text = ' '.join(message.text.split()[1:])
        sent_count = 0
        for user_id in user_data:
            try:
                bot.send_message(chat_id=user_id, text=message_text)
                sent_count += 1
            except telebot.apihelper.ApiTelegramException as e:
                logging.warning(f"Could not send message to {user_id}: {e}")
        try:
            bot.send_message(message.chat.id, f"Broadcast sent to {sent_count} users.")
        except telebot.apihelper.ApiTelegramException as e:
            logging.error(f"Failed to send broadcast confirmation to owner: {e}")
    else:
        try:
            bot.send_message(message.chat.id, "You are not authorized to use this command.")
        except telebot.apihelper.ApiTelegramException as e:
            logging.error(f"Failed to send unauthorized message to user {message.from_user.id}: {e}")

@bot.message_handler(commands=['stats'])
def stats(message: telebot.types.Message):
    user_count = len(user_data)
    try:
        bot.send_message(message.chat.id, f"Total users who started the bot: {user_count}")
    except telebot.apihelper.ApiTelegramException as e:
        logging.error(f"Failed to send stats to user {message.from_user.id}: {e}")

def main():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Bot polling failed: {e}")
            bot.send_message(
                chat_id=LOG_GROUP_ID,
                text=f"Bot polling failed: {e}"
            )
            time.sleep(10)  # Wait before restarting the polling loop

if __name__ == "__main__":
    main()
    
