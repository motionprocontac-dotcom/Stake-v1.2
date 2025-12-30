
import os
import feedparser
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import threading

# --- CONFIG ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_EN = os.getenv("CHANNEL_EN")
BTC_WALLET = os.getenv("BTC_WALLET")
ETH_WALLET = os.getenv("ETH_WALLET")
LTC_WALLET = os.getenv("LTC_WALLET")
STAKE_AFFILIATE = os.getenv("STAKE_AFFILIATE")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

RSS_STAKE_COM = "https://www.reddit.com/r/stakecom/new/.rss"
RSS_STAKE_US = "https://www.reddit.com/r/stakeus/new/.rss"

# --- BOT FUNCTIONS ---
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Stake.com News", callback_data='stake_com')],
        [InlineKeyboardButton("Stake US News", callback_data='stake_us')],
        [InlineKeyboardButton("Estimate Monthly", callback_data='estimate')],
        [InlineKeyboardButton("Support / Donations", callback_data='support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome! Choose a category:", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == "stake_com":
        posts = get_rss_posts(RSS_STAKE_COM)
        text = "\n\n".join(posts)
        query.edit_message_text(text=text[:4000])
    elif data == "stake_us":
        posts = get_rss_posts(RSS_STAKE_US)
        text = "\n\n".join(posts)
        query.edit_message_text(text=text[:4000])
    elif data == "estimate":
        query.edit_message_text("Estimation tool coming soon...")
    elif data == "support":
        text = f"BTC: {BTC_WALLET}\nETH: {ETH_WALLET}\nLTC: {LTC_WALLET}\nAffiliate: {STAKE_AFFILIATE}"
        query.edit_message_text(text=text)

def get_rss_posts(url):
    feed = feedparser.parse(url)
    posts = []
    for entry in feed.entries[:5]:
        posts.append(f"{entry.title}\n{entry.link}")
    return posts

def job_rss(bot):
    for rss_url in [RSS_STAKE_COM, RSS_STAKE_US]:
        posts = get_rss_posts(rss_url)
        text = "\n\n".join(posts)
        bot.send_message(chat_id=CHANNEL_EN, text=text[:4000])

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CallbackQueryHandler(button))

scheduler = BackgroundScheduler()
scheduler.add_job(lambda: job_rss(updater.bot), 'interval', minutes=15)
scheduler.start()

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=5000)

threading.Thread(target=run).start()

updater.start_polling()
updater.idle()
