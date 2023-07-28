import asyncio
import discord
import numpy as np
from anime_recommender.data import generate_query_response, handle_recommendation_request, handle_search_query, initialize_recommender
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
        query_list = handle_search_query(args)
        if len(query_list) > 1:
            try:
                await ctx.send('Multiple search results for the title: ' + args + '. Please select the correct one by typing the number next to it.\n')
                await ctx.send(generate_query_response(query_list))
                msg = await client.wait_for("message", timeout=30)
                selected_index = int(msg.content)
                index = query_list.loc[query_list['SelectionIndex'] == selected_index].index.astype(int)[0]
                await ctx.send(handle_recommendation_request(index))
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time!")
        elif len(query_list) == 1:
            index = query_list.loc[query_list['SelectionIndex'] == 1].index.astype(int)[0]
            await ctx.send(handle_recommendation_request(index))
        else:
            await ctx.send('No Matching Anime Found In Database')

    @client.command(name='waifu')
    async def waifu(ctx, *args):
        await ctx.send(get_waifu_payload(args))

    @client.command(name='lonely')
    async def lonely(ctx, *, args):
        await ctx.send(gamer_girl_gpt_response(args))

    client.run(TOKEN)