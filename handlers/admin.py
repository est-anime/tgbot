from telegram.ext import CommandHandler
from config import ADMIN_USER_ID
from utils.mongodb import add_banned_user, remove_banned_user, is_banned, get_all_users

def is_admin(user_id):
    return user_id == ADMIN_USER_ID

def list_users(update, context):
    if not is_admin(update.message.from_user.id):
        update.message.reply_text('You are not authorized to use this command.')
        return
    
    users = get_all_users()
    if not users:
        update.message.reply_text('No users have interacted with the bot yet.')
    else:
        user_list = '\n'.join([f"ID: {user['user_id']}, Username: {user.get('username', 'N/A')}" for user in users])
        update.message.reply_text('Users who have interacted with the bot:\n' + user_list)

def private_message(update, context):
    if not is_admin(update.message.from_user.id):
        update.message.reply_text('You are not authorized to use this command.')
        return
    
    try:
        user_id = int(context.args[0])
        message = ' '.join(context.args[1:])
        context.bot.send_message(chat_id=user_id, text=message)
        update.message.reply_text('Message sent.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /privatemsg <user_id> <message>')

def ban_user(update, context):
    if not is_admin(update.message.from_user.id):
        update.message.reply_text('You are not authorized to use this command.')
        return
    
    try:
        user_id = int(context.args[0])
        add_banned_user(user_id)
        update.message.reply_text(f'User {user_id} has been banned.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /ban <user_id>')

def unban_user(update, context):
    if not is_admin(update.message.from_user.id):
        update.message.reply_text('You are not authorized to use this command.')
        return
    
    try:
        user_id = int(context.args[0])
        remove_banned_user(user_id)
        update.message.reply_text(f'User {user_id} has been unbanned.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /unban <user_id>')

list_users_handler = CommandHandler("listusers", list_users)
private_message_handler = CommandHandler("privatemsg", private_message)
ban_user_handler = CommandHandler("ban", ban_user)
unban_user_handler = CommandHandler("unban", unban_user)
