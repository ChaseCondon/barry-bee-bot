# bot.py
import os
import sys
import random

import pyowm
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWM_KEY = os.getenv('OWM_KEY')

client = discord.Client()
bot = commands.Bot(command_prefix='!')


@bot.command(name='blocks', help='Adds some blocks.')
async def blocks(ctx, *words):
    seq = []
    for word in words:
        for letter in word:
            if letter.isalpha():
                seq.append(f':regional_indicator_{letter.lower()}:')
            else:
                seq.append(letter)
        seq.append(' ' * 10)

    await ctx.send(' '.join(seq))


@bot.command(name='choose', help='Choose [A] or [B] or...')
async def choose(ctx, *choices):
    choices = [choice for choice in choices if choice != 'or']
    choice = random.choice(choices)
    await ctx.send(choice)


@bot.command(name='clap', help='Adds the clap emoji between each word.')
async def clap(ctx, *words):
    resp = ' :clap: '.join(words)
    await ctx.send(resp)


@bot.command(name='coin', help='Flips a coin.')
async def coin(ctx):
    choice = random.randint(0, 1)
    await ctx.send('Heads' if choice == 1 else 'Tails')


@bot.command(name='echo', help='Repeats what you say.')
async def echo(ctx, *words):
    await ctx.send(' '.join(words))


@bot.command(name='randomnumber', help='Picks a random number.')
async def random_number(ctx, max_val=sys.maxsize):
    choice = random.randint(0, float(max_val))
    await ctx.send(f'I pick {choice}')


@bot.command(name='roll', help='Rolls a die of given sides.')
async def roll_die(ctx, num_sides=20):
    choice = random.randint(1, num_sides)
    await ctx.send(f'You rolled a {choice}')


@bot.command(name='taps', help="Tells you if it's taps aff.")
async def taps(ctx):
    weather_emoji = {
        'clear sky': ':sunny:',
        'few clouds': ':white_sun_cloud:',
        'scattered clouds': ':cloud:',
        'broken clouds': ':cloud:',
        'shower rain': ':cloud_rain:',
        'rain': ':white_sun_rain_cloud:',
        'thunderstorm': ':cloud_lightning:',
        'snow': ':cloud_snow:',
        'mist': ':cloud_rain:'
    }

    owm = pyowm.OWM(OWM_KEY)
    observation = owm.weather_at_place('Glasgow,UK')
    w = observation.get_weather()
    status = w.get_detailed_status()

    if status != 'clear sky':
        msg = 'Taps oan'
    else:
        msg = 'Taps aff'

    await ctx.send(f'{weather_emoji[status]} {msg} {weather_emoji[status]}')


@bot.command(name='teams', help='Assigns players into teams')
async def teams(ctx, *players):
    players = list(players)
    random.shuffle(players)
    team_one = '\n\t'.join(players[:int(len(players)/2)])
    team_two = '\n\t'.join(players[int(len(players)/2):])

    msg = f'Team One:\n\t{team_one}\n\nTeam Two:\n\t{team_two}'
    await ctx.send(msg)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == 'same':
        await message.channel.send('Same')


bot.run(TOKEN)
client.run(TOKEN)
