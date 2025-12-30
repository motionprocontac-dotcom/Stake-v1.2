
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_EN = os.getenv("CHANNEL_EN")

BTC_WALLET = os.getenv("BTC_WALLET")
ETH_WALLET = os.getenv("ETH_WALLET")
LTC_WALLET = os.getenv("LTC_WALLET")

STAKE_AFFILIATE = os.getenv("STAKE_AFFILIATE")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

RSS_STAKE_COM = "https://www.reddit.com/r/stakecom/new/.rss"
RSS_STAKE_US = "https://www.reddit.com/r/stakeus/new/.rss"
