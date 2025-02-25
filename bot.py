import tweepy
import discord
import os
from discord.ext import tasks
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials (ensure to set up your own API keys on Twitter Developer Platform)
CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Ensure that the keys are loaded correctly
print("Twitter Consumer Key:", CONSUMER_KEY)
print("Twitter Consumer Secret:", CONSUMER_SECRET)

# Set up Twitter API client
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# BOT CONFIGURATION
TOKEN = ("MTM0Mzc1NzUyODkyNzgzMDAyNg.GXJo4G.-xDLQV8GalG7Hz1Epj8vGEowViBz6boBONJzDw")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
TWITTER_USERNAMES = [
    "WhatcherGuru", "DailyMailCeleb",
    "Nuotrix", "PFTrenches", "TrumpDailyPosts", "meme1coins",
    "phantom", "orangiecoins", "solana", "binance", "CryptoXEmperor",
    "BoredElonMusk", "Cobratate", "BillGates", "realDonaldTrump"
]

# Set up bot with appropriate intents
intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    if not check_tweets.is_running():
        check_tweets.start()

# Store last seen tweet links
last_tweets = {}

@tasks.loop(seconds=30)
async def check_tweets():
    """Fetches tweets from Twitter API and posts new ones to the Discord channel."""
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("Channel not found! Check if the bot has access.")
        return

    for username in TWITTER_USERNAMES:
        try:
            # Fetch latest tweet from user
            tweets = api.user_timeline(screen_name=username, count=1, tweet_mode='extended')
            if not tweets:
                print(f"No tweets found for @{username}")
                continue

            latest_tweet = tweets[0]
            tweet_link = f"https://twitter.com/{username}/status/{latest_tweet.id}"

            # Only post if the tweet is new
            if username not in last_tweets or last_tweets[username] != tweet_link:
                last_tweets[username] = tweet_link
                await channel.send(f"New tweet from @{username}: {tweet_link}")

        except tweepy.TweepError as e:
            print(f"Error fetching tweets for @{username}: {e}")

if __name__ == "__main__":
    client.run(TOKEN)
