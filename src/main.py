import discord
import re

GUILD_ID = discord.Object(id=1197324475851620383)

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author.bot:
            return
        
        matches = re.findall(r"\[\[(.*?)\]\]", message.content)

        if matches:
            await message.channel.send(f"Found matches: {', '.join(matches)}")
        

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)


client = Client(intents=intents)
client.run('')
