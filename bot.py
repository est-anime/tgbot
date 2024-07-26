from telegram.ext import Updater
from config import TOKEN
from handlers import commands, callbacks, admin

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(commands.start_handler)
    dp.add_handler(commands.help_handler)
    dp.add_handler(commands.info_handler)
    dp.add_handler(commands.time_handler)
    dp.add_handler(commands.joke_handler)
    dp.add_handler(commands.userid_handler)
    dp.add_handler(commands.weather_handler)
    dp.add_handler(commands.quote_handler)
    dp.add_handler(admin.list_users_handler)
    dp.add_handler(admin.private_message_handler)
    dp.add_handler(admin.ban_user_handler)
    dp.add_handler(admin.unban_user_handler)

    # Add callback query handler
    dp.add_handler(callbacks.help_button_handler)

    # Add message handler for non-command messages
    dp.add_handler(commands.echo_handler)

    # Save chat IDs to broadcast later
    dp.bot_data['chat_ids'] = set()

    # Update chat IDs on any message
    def update_chat_ids(update, context):
        context.bot_data['chat_ids'].add(update.message.chat_id)
    dp.add_handler(MessageHandler(Filters.text, update_chat_ids))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
