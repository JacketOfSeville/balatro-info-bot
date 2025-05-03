import discord
import re
import os

from dotenv import load_dotenv
from builder import build_reply

load_dotenv()
TOKEN = os.getenv('TOKEN')

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author.bot:
            return
        
        matches = re.findall(r"\[\[(.*?)\]\]", message.content)
        if matches:
            for match in matches:
                print(f"Deteced: {match}")
                result = build_reply(match)
                if result:
                    if result["category"] == 'jokers':
                        rarity = result.get('rarity', 'Common')
                        unlock = result.get('unlock', 'Available from the start')
                        image = result.get('image')

                        embed = discord.Embed(
                            colour=discord.Colour.red(),
                            description = rarity+" Joker",
                            title = result['name']
                        )
                        if image:
                            embed.set_thumbnail(url = result["image"])

                        embed.set_footer(text = "cooter")
                        embed.set_author(name = "Balatro Informa")
                        
                        embed.add_field(name = "Effect",value = result["text"])
                        embed.add_field(name = "Unlocked by",value = unlock)

                        await message.reply(embed=embed)
                    elif result["category"] == 'vouchers':
                        unlock = result.get('unlock', 'Available from the start')
                        image = result.get('image')

                        embed = discord.Embed(
                            colour=discord.Colour.green(),
                            description = "Voucher",
                            title = result['name']
                        )
                        if image:
                            embed.set_thumbnail(url = result["image"])

                        embed.set_footer(text = "cooter")
                        embed.set_author(name = "Balatro Information Bot")
                        
                        embed.add_field(name = "Effect",value = result["text"])
                        embed.add_field(name = "Unlocked by",value = unlock)

                        await message.reply(embed=embed)
        

intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix="!", intents=intents)
client = Client(intents=intents)
client.run(TOKEN)
