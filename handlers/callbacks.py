from telegram.ext import CallbackQueryHandler

def button(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'show_help':
        query.edit_message_text(text='Here are the available commands:\n'
                                     '/start - Start the bot\n'
                                     '/help - Get help\n'
                                     '/info - Get information\n'
                                     '/time - Get current server time\n'
                                     '/joke - Get a random joke\n'
                                     '/userid - Get your user ID')

help_button_handler = CallbackQueryHandler(button)
