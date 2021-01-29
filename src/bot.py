import aiohttp
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

# What the bot will say and what it will look for to reset the timer
to_say = "Hi, this is a test"

# The time between each time the bot will say something
# The arguments should not be confusing
timer = timedelta(days=0, seconds=10, microseconds=0,
                  milliseconds=0, minutes=0, hours=0, weeks=0)


class BotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, command_prefix="sudo ")

        # Set the last time to the current time
        self.last_time = datetime.now()

        # Make a background task of the thing
        self.bg_task = self.say_message.start()

    async def on_ready(self):
        # Start the bot up
        self.http_client = aiohttp.ClientSession()

        # Setting the last time to now once again
        self.last_time = datetime.now()

        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print(discord.utils.oauth_url(self.user.id))

    async def on_message(self, message: discord.message):
        # If the message starts with the query, do things
        # Also I'm sorry
        if message.content.lower().startswith(to_say.lower()):
            # Set the last time the looked-for message was sent
            self.last_time = message.created_at

        # Keep this
        await self.process_commands(message)

    async def get_time_passed(self):
        # Get how much time has passed since the looked-for message was sent
        return (datetime.utcnow() - self.last_time).total_seconds()

    @tasks.loop(seconds=timer.total_seconds() / 2)
    async def say_message(self):
        # Wait until the bot has started up
        await self.wait_until_ready()
        
        # Just for some debugging purposes
        # print(await self.get_time_passed())
        
        # If the timer is up, send the thing
        if await self.get_time_passed() >= timer.total_seconds():
            await self.get_channel(637316663267819561).send(to_say)


# Get the token
with open("token.txt", 'r') as file:
    TOKEN = file.read().strip()

# Create and instance of our bot class
bot = BotClient()
# Hey, kids, this is running a self-bot. It's (generally) against TOS!
# bot.run(TOKEN, bot=False)

# This is how me run an actual bot
bot.run(TOKEN)
