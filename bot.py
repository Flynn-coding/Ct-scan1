import discord
import feedparser
import os
from discord.ext import tasks

# BOT CONFIGURATION (Using Environment Variables for Security)
TOKEN = os.getenv("TOKEN")  # Set this in Railway
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Set this in Railway
TWITTER_USERNAMES = ["elonmusk", "MarioNawfal", "WhatcherGuru", "DailyMailCeleb", 
                     "Nuotrix", "PFTrenches", "TrumpDailyPosts", "meme1coins", 
                     "phantom", "orangiecoins", "solana", "binance", "CryptoXEmperor", 
                     "BoredElonMusk", "Cobratate", "BillGates", "realDonaldTrump"]  

# RSSHub URL (Used to bypass Twitter API limits)
RSS_URL = "https://rsshub.app/twitter/user/{}"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    if not check_tweets.is_running():
        check_tweets.start()

# Store last seen tweet links
last_tweets = {}

@tasks.loop(seconds=5)
async def check_tweets():
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("Channel not found!")
        return

    for username in TWITTER_USERNAMES:
        feed = feedparser.parse(RSS_URL.format(username))
        if not feed.entries:
            continue

        latest_tweet = feed.entries[0]
        tweet_link = latest_tweet.link

        if username not in last_tweets or last_tweets[username] != tweet_link:
            last_tweets[username] = tweet_link
            await channel.send(f"New tweet from @{username}: {tweet_link}")

client.run(TOKEN)

if __name__ == "__main__":
    client.run(TOKEN)
