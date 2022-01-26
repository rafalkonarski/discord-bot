import discord
from discord.ext import commands
import random
import praw
import requests
import os
import asyncio

#prefix for bot
client = commands.Bot(command_prefix='.')

#bot online status
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('bot working'))
    print("Bot is ready!")

#information about reddit bot
reddit = praw.Reddit(client_id='d5_6ppUPupU6Ql23A9i0uw',
                     client_secret='Lw2sh_OkEProI1GOa1zf_Rh0SorRhA',
                     user_agent='python_praw',
                     check_for_async=False)

#bot hits designated user
punch_gifs = ['https://c.tenor.com/CRl-iJT02YIAAAAC/naruto-nine-tails.gif']
punch_names = ['Punches You!']
@client.command()
async def punch(ctx):
    embed = discord.Embed(
        colour = (discord.Colour.random()),
        description = f"{ctx.author.mention} {(random.choice(punch_names))}"
    )
    embed.set_image(url=(random.choice(punch_gifs)))

    await ctx.send(embed=embed)

#a simple game in ping pong
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong!')

#reddit meme bot
@client.command()
async def memes(ctx):
    ctx = client.get_channel(933762162936139886)
    memes_subsmissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1,20)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_subsmissions if not x.stickied)

    await ctx.send(submission.url)

#reddit random jokes
@client.command()
async def jokes(ctx):
    ctx = client.get_channel(935898462443151391)
    memes_subsmissions = reddit.subreddit('jokes').hot()
    post_to_pick = random.randint(1,20)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_subsmissions if not x.stickied)

    await ctx.send(submission.selftext)
    await ctx.send(submission.url)


#bot clear messages
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

#giving any arguments
@client.command()
async def arg(ctx, arg1, arg2):
    await ctx.send('You passed {} and {}'.format(arg1, arg2))

#math operations
@client.command()
async def add(ctx, a: int, b: int):
    await ctx.send({a + b})

@client.command()
async def sub(ctx, a: int, b: int):
    await ctx.send({a - b})

#bot checks and kick if you are bot
@client.command()
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
    ctx = client.get_channel(935893608970748014)
    if not user.bot:
        await user.kick(reason=reason)
        await ctx.send(f"Successfully kicked {user}!")
    else:
        await ctx.send("You can't kick a bot!")

#simple game in 8ball
@client.command(aliases=['8ball', '8b'])
async def eightball(ctx, *, question):
    responses = ["Yes.",
                 "No.",
                 "Maybe.",
                 "Maybe not.",
                 "What you want from me?",
                 "I don't have time now, try again later."]
    await ctx.send(f':8ball: Question:  {question}\n:8ball: Answer: {random.choice(responses)}')

#bot join to the channel
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


client.run('')
