import telebot


def publish_in_telegram(pd, channel_id, message, parse_mode=None):
    token = pd.inputs["telegram_bot_api"]["$auth"]["token"]
    bot = telebot.TeleBot(token=token, parse_mode=None)
    bot.send_message(channel_id, message, parse_mode=parse_mode)
