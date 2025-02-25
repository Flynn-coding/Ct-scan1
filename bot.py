import discord
import feedparser
import os
import asyncio
from discord.ext import tasks

# BOT CONFIGURATION (Using Environment Variables for Security)
TOKEN = os.getenv("DISCORD_TOKEN")  # Set this in Railway
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Set this in Railway
TWITTER_USERNAMES = [
    "WhatcherGuru", "DailyMailCeleb", 
    "Nuotrix", "PFTrenches", "TrumpDailyPosts", "meme1coins", 
    "phantom", "orangiecoins", "solana", "binance", "CryptoXEmperor", 
    "BoredElonMusk", "Cobratate", "BillGates", "realDonaldTrump"
]

# RSSHub URL (Used to bypass Twitter API limits)
RSS_URL = "https://rsshub.app/twitter/user/{}"

# Set up bot with appropriate intents
intents = discord.Intents.default()
intents.guilds = True  # Required for channel fetching
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    if not check_tweets.is_running():
        check_tweets.start()
    if not keep_alive.is_running():
        keep_alive.start()

# Store last seen tweet links
last_tweets = {}

@tasks.loop(seconds=30)  # Adjust to prevent rate limits
async def check_tweets():
    """Fetches tweets from RSS and posts new ones to the Discord channel."""
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("Channel not found! Check if the bot has access.")
        return

    for username in TWITTER_USERNAMES:
        try:
            feed = feedparser.parse(RSS_URL.format(username))
            print(f"Feed data for @{username}: {feed}")  # Log the full feed data

            if not feed.entries:
                print(f"No tweets found for @{username}")
                continue

            # Debug: print each entry to see what's inside
            for entry in feed.entries:
                print(f"Entry found: {entry}")

            latest_tweet = feed.entries[0]
            tweet_link = latest_tweet.get("link")
            
            if tweet_link:
                # Only post if the tweet is new
                if username not in last_tweets or last_tweets[username] != tweet_link:
                    last_tweets[username] = tweet_link
                    # Send the tweet link to the Discord channel
                    await channel.send(f"New tweet from @{username}: {tweet_link}")
                    print(f"Tweet sent to Discord: {tweet_link}")
            else:
                print(f"Missing tweet link for @{username}")

        except Exception as e:
            print(f"Error fetching tweets for @{username}: {e}")

@tasks.loop(minutes=5)
async def keep_alive():
    print("🔄 Keeping bot alive...")

if __name__ == "__main__":
    client.run(TOKEN)
