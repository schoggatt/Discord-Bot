import discord
from anime_recommender.data import handle_recommendation_request, initialize_recommender
from gamer_girl_gpt import gamer_girl_gpt_response
from waifu_api.waifu import get_waifu_payload
from config import get_discord_token
from discord.ext import commands
from discord.ext.commands import Bot

async def send_message(message, is_private):
    try:
        await message.author.send(message) if is_private else await message.channel.send(message)
    except Exception as e:
        print(e)

def run_discord_bot():
    initialize_recommender()
    TOKEN = get_discord_token()
    intents = discord.Intents.default()
    intents.message_content = True
    client = Bot(command_prefix='!', intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.command(name='recommend')
    async def recommend(ctx,* , args):
        await ctx.send(handle_recommendation_request(args))

    @client.command(name='waifu')
    async def waifu(ctx, *args):
        await ctx.send(get_waifu_payload(args))

    @client.command(name='lonely')
    async def lonely(ctx, *, args):
        await ctx.send(gamer_girl_gpt_response(args))

    client.run(TOKEN)