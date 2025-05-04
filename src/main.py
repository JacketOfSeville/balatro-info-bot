import discord
import re
import os

from dotenv import load_dotenv
from builder import build_reply

load_dotenv()
TOKEN = os.getenv('TOKEN')

AUTHOR = 'Balatro Information Bot'
FOOTER = 'Data extracted from game files'

DEFALT_RARITY = 'Common'
DEFALT_UNLOCK = 'Available from the start'

CATEGORIES_TO_COLORS = {
    "jokers": discord.Colour.red(),
    "vouchers": discord.Colour.green(),
    "blinds": discord.Colour.orange(),
    "tarots": discord.Colour.purple(),
    "spectrals": discord.Colour.dark_blue(),
    "planets": discord.Colour.blue()
}

def append_unlocked_by(card, _):
    return discord.Embed(
        colour=discord.Colour.red(),
        description=card.get('rarity', DEFALT_RARITY)+' Joker',
        title=card['name']
    ).add_field(
        name='Unlocked by',
        value=card.get('unlock', DEFALT_UNLOCK)
    )

def append_embed_for_blinds(blind, _):
    return discord.Embed(
        colour=discord.Colour.orange(),
        description=blind.get('boss', '')+'Boss Blind',
        title=blind['name']
    )

CATEGORIES_TO_EMBED_APPENDER = {
    "jokers": append_unlocked_by,
    "vouchers": append_unlocked_by,
    "blinds": append_embed_for_blinds,
}

def build_embed_for_unknown(match):
    embed = discord.Embed(
        colour=discord.Colour.darker_grey(),
        description='Item not found in the database',
        title=match
    )

    return embed

def build_embed_for_card(card):
    card_category = card['category']

    embed = discord.Embed(
        colour=CATEGORIES_TO_COLORS[card_category],
        description=card_category,
        title=card['name']
    )

    appender = CATEGORIES_TO_EMBED_APPENDER.get(card_category)
    if appender is not None:
        embed = appender(card, embed)

    image = card.get('image')
    if image is not None:
        embed.set_thumbnail(url=image)

    embed.set_footer(text=FOOTER)
    embed.set_author(name=AUTHOR)
    embed.add_field(name='Effect', value=card['text'])

    return embed

class Client(discord.Client):
    def choose_embed(self, match):
        card = build_reply(match)

        return build_embed_for_unknown(match) if card is None else build_embed_for_card(card)

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author.bot:
            return
        
        matches = re.findall(r'\[\[(.*?)\]\]', message.content)

        if not matches:
            return
        
        embeds = [self.choose_embed(match) for match in matches]

        await message.reply(embeds=embeds[:10])

intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix='!', intents=intents)
client = Client(intents=intents)
client.run(TOKEN)
