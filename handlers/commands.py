from telegram.ext import CommandHandler, MessageHandler, Filters
from datetime import datetime
import requests
from config import WEATHER_API_KEY
from utils.helpers import get_weather, get_quote
from utils.mongodb import add_user, is_banned

def start(update, context):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    if is_banned(user_id):
        update.message.reply_text('You are banned from using this bot.')
        return
    
    add_user(user_id, username)
    update.message.reply_text('Hello! I am your bot. How can I help you today?')
    show_help_button(update, context)

def help_command(update, context):
    update.message.reply_text('Here are the available commands:\n'
                              '/start - Start the bot\n'
                              '/help - Get help\n'
                              '/info - Get information\n'
                              '/time - Get current server time\n'
                              '/joke - Get a random joke\n'
                              '/userid - Get your user ID\n'
                              '/weather <city> - Get the current weather\n'
                              '/quote - Get a random quote')

def info(update, context):
    user = update.message.from_user
    update.message.reply_text(f'Hello {user.first_name}! Your username is @{user.username}.')

def time(update, context):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update.message.reply_text(f'Current server time is {now}.')

def joke(update, context):
    joke = requests.get('https://official-joke-api.appspot.com/random_joke').json()
    update.message.reply_text(f'{joke["setup"]}\n{joke["punchline"]}')

def userid(update, context):
    user_id = update.message.from_user.id
    update.message.reply_text(f'Your user ID is {user_id}.')

def weather(update, context):
    if len(context.args) == 0:
        update.message.reply_text('Please specify a city.')
        return
    city = ' '.join(context.args)
    weather_info = get_weather(city, WEATHER_API_KEY)
    update.message.reply_text(weather_info)

def quote(update, context):
    quote_text = get_quote()
    update.message.reply_text(quote_text)

def echo(update, context):
    update.message.reply_text(update.message.text)

def show_help_button(update, context):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [[InlineKeyboardButton("Show Commands", callback_data='show_help')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Need help? Click the button below:', reply_markup=reply_markup)

start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help_command)
info_handler = CommandHandler("info", info)
time_handler = CommandHandler("time", time)
joke_handler = CommandHandler("joke", joke)
userid_handler = CommandHandler("userid", userid)
weather_handler = CommandHandler("weather", weather)
quote_handler = CommandHandler("quote", quote)
echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)
