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
        
        matches = re.findall(r'\[\[(.*?)\]\]', message.content)
        if matches:
            embeds = []
            author = 'Balatro Information Bot'
            footer = 'Data extracted from game files'

            for match in matches:
                print(f'Deteced: {match}')
                result = build_reply(match)
                if result:
                    if result['category'] == 'jokers':
                        rarity = result.get('rarity', 'Common')
                        unlock = result.get('unlock', 'Available from the start')
                        image = result.get('image')

                        embed = discord.Embed(
                            colour=discord.Colour.red(),
                            description = rarity+' Joker',
                            title = result['name']
                        )
                        if image:
                            embed.set_thumbnail(url = result['image'])

                        embed.set_footer(text = footer)
                        embed.set_author(name = author)
                        
                        embed.add_field(name = 'Effect',value = result['text'])
                        embed.add_field(name = 'Unlocked by',value = unlock)

                        embeds.append(embed)
                    elif result['category'] == 'vouchers':
                        unlock = result.get('unlock', 'Available from the start')
                        image = result.get('image')

                        embed = discord.Embed(
                            colour=discord.Colour.green(),
                            description = 'Voucher',
                            title = result['name']
                        )
                        if image:
                            embed.set_thumbnail(url = result['image'])

                        embed.set_footer(text = footer)
                        embed.set_author(name = author)
                        
                        embed.add_field(name = 'Effect',value = result['text'])
                        embed.add_field(name = 'Unlocked by',value = unlock)

                        embeds.append(embed)
                    elif result['category'] == 'blinds':
                        image = result.get('image')
                        boss = result.get('boss', '')

                        embed = discord.Embed(
                            colour=discord.Colour.orange(),
                            description = boss+'Boss Blind',
                            title = result['name']
                        )
                        if image:
                            embed.set_thumbnail(url = result['image'])

                        embed.set_footer(text = footer)
                        embed.set_author(name = author)
                        
                        embed.add_field(name = 'Effect',value = result['text'])

                        embeds.append(embed)
                    elif result['category'] == 'tarots':
                        image = result.get('image')

                        embed = discord.Embed(
                            colour=discord.Colour.purple(),
                            description = 'Tarot Card',
                            title = result['name']
                        )
                        if image:
                            embed.set_thumbnail(url = result['image'])

                        embed.set_footer(text = footer)
                        embed.set_author(name = author)
                        
                        embed.add_field(name = 'Effect',value = result['text'])

                        embeds.append(embed)
                    elif result['category'] == 'spectrals':
                        image = result.get('image')

                        embed = discord.Embed(
                            colour=discord.Colour.dark_blue(),
                            description = 'Spectral Card',
                            title = result['name']
                        )
                        if image:
                            embed.set_thumbnail(url = result['image'])

                        embed.set_footer(text = footer)
                        embed.set_author(name = author)
                        
                        embed.add_field(name = 'Effect',value = result['text'])

                        embeds.append(embed)
                    elif result['category'] == 'planets':
                        image = result.get('image')

                        embed = discord.Embed(
                            colour=discord.Colour.blue(),
                            description = 'Planet Card',
                            title = result['name']
                        )
                        if image:
                            embed.set_thumbnail(url = result['image'])

                        embed.set_footer(text = footer)
                        embed.set_author(name = author)
                        
                        embed.add_field(name = 'Effect',value = result['text'])

                        embeds.append(embed)
                    else:
                        print('Unknown Item')
                else:
                    embed = discord.Embed(
                        colour=discord.Colour.darker_grey(),
                        description = 'Item not found in the database',
                        title = match
                    )

                    embed.set_footer(text = footer)
                    embed.set_author(name = author)

                    embeds.append(embed)                    

            await message.reply(embeds=embeds[:10])
        

intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix='!', intents=intents)
client = Client(intents=intents)
client.run(TOKEN)
