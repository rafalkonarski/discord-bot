import discord
from discord.ext import commands
import random
import praw
import requests
import os
import asyncio

#prefix for bot
client = commands.Bot(command_prefix='.')

api_key = "d0d1c8f0f78774930da40b6bc6ffdd3e"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

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
punch_names = ['Punches you!']
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
    ctx = client.get_channel(935935329758765186)
    memes_subsmissions = reddit.subreddit('overwatch_memes').hot()
    post_to_pick = random.randint(1,50)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_subsmissions if not x.stickied)

    await ctx.send(submission.url)

#reddit random jokes
@client.command()
async def jokes(ctx):
    ctx = client.get_channel(935935329758765186)
    memes_subsmissions = reddit.subreddit('jokes').hot()
    post_to_pick = random.randint(1,20)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_subsmissions if not x.stickied)

    await ctx.send(submission.selftext)


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

#bot shows the weather in selected city
@client.command()
async def weather(ctx, *, city: str):
        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        channel = ctx.message.channel
        if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_temperature_celsiuis = str(round(current_temperature - 273.15))
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                embed = discord.Embed(
                    title=f"WEATHER FORECAST - {city_name}",
                    color=0x7289DA,
                    timestamp=ctx.message.created_at,
                )
                embed.add_field(
                    name="DESCRIPTION",
                    value=f"**{weather_description}**",
                    inline=False)
                embed.add_field(
                    name="TEMPERATURE(C)",
                    value=f"**{current_temperature_celsiuis}??C**",
                    inline=False)
                embed.add_field(
                    name="HUMIDITY(%)", value=f"**{current_humidity}%**", inline=False)
                embed.add_field(
                    name="ATMOSPHERIC PRESSURE(hPa)",
                    value=f"**{current_pressure}hPa**",
                    inline=False)
                embed.set_footer(text=f"Requested by {ctx.author.name}")
                await channel.send(embed=embed)
        else:
                await channel.send(f"There was no results about this place!")


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
