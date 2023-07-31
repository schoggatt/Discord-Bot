import asyncio
import discord
from anime_recommender.data import generate_query_response, handle_recommendation_request, handle_search_query, initialize_recommender
from gamer_girl_gpt import gamer_girl_gpt_response
from spotify.setup import get_spotify_token
from waifu_api.waifu import get_waifu_payload
from config import get_discord_token
from discord.ext import commands
from discord.ext.commands import Bot
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL
import discord.voice_client
from discord.utils import get

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

song_queue = []

def run_discord_bot():
    initialize_recommender()
    get_spotify_token()
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
        # We only want to send a message for selection if there is more than one result
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
        # If there is only one then we just use that one
        elif len(query_list) == 1:
            index = query_list.loc[query_list['SelectionIndex'] == 1].index.astype(int)[0]
            await ctx.send(handle_recommendation_request(index))
        # Otherwise just notify it isnt in the list
        else:
            await ctx.send('No Matching Anime Found In Database')

    @client.command(name='waifu')
    async def waifu(ctx, *args):
        await ctx.send(get_waifu_payload(args))

    @client.command(name='lonely')
    async def lonely(ctx, *, args):
        await ctx.send(gamer_girl_gpt_response(args))

    # TODO: This could be seperated into a different file that can handle different sources
    # TODO: Add a queue system
    @client.command(name='play')
    async def play(ctx, *args):
        url = args[0]
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice is None:
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                await ctx.send("Join a voice channel first")
                return
            await voice_channel.connect()

        ydl_opts = {'format': 'bestaudio'}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            song_url = info['formats'][3]['url']

        song_queue.append(song_url)

        voice = get(client.voice_clients, guild=ctx.guild)
        if not ctx.voice_client.is_playing():
            queued_song_url = song_queue.pop(0)
            voice.play(FFmpegPCMAudio(queued_song_url, **FFMPEG_OPTIONS), after= lambda x: play_next(ctx))
        else:
            await ctx.send("Added to queue...")

    def play_next(ctx):
        voice = get(client.voice_clients, guild=ctx.guild)
        if len(song_queue) > 0:
            voice.play(FFmpegPCMAudio(song_queue.pop(0), **FFMPEG_OPTIONS), after=lambda x: play_next(ctx))


    @client.command(name='pause')
    async def pause(ctx):
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing.")

    @client.command(name='resume')
    async def resume(ctx):
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")

    @client.command(name='disconnect')
    async def disconnect(ctx):
        song_queue.clear()
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    client.run(TOKEN)