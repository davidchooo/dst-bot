import os

from discord.ext import commands
from dotenv import load_dotenv
import json
import shutil
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DST_DIR = os.getenv('DST_DIR')
BACKUP_DIR = os.getenv('BACKUP_DIR')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command(aliases=['clops'])
async def deerclops(ctx, *args):
    with open('data/deerclops.txt', 'r+') as f:
        day = f.readlines()[0].strip()
        if (not len(args)):
            await ctx.send(f'Deerclops will spawn on Day {day}.')
        elif (args[0] == 'help'):
            await ctx.send('Deerclops Usage: ')
        elif (len(args) == 1):
            # Update file
            day += 71.8
            await ctx.send(f'Updated: Deerclops will spawn on Day {args[0]}.')
        else:
            await ctx.send('Only provide 1 argument! e.g. "!deerclops 10"')


@bot.command(aliases=['mod'])
async def mods(ctx, *args):
    with open('data/mods.json', 'r+') as f:
        data = json.load(f)

        # Display mods
        if (not len(args)):
            message = ''

            # Add server mods
            message += '__**Server Mods:**__\n'
            for mod in data['server']:
                message += f'- {mod}\n'

            # Add client mods
            message += '\n__**Client Mods:**__\n'
            for mod in data['client']:
                message += f'- {mod}\n'

            await ctx.send(message)

        # Add new mod
        elif (args[0] == 'server' or args[0] == 'client'):
            mod_type = args[0]

            # Format the mod and add it to json
            mod = ' '.join(args[1:])
            data[mod_type].append(mod)

            # Clear the json file before dumping the updated contents
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)

            # Send confirmation!
            await ctx.send(f'Added "{mod}" to {mod_type} mods!')

        # Help
        elif (args[0] == 'help'):
            await ctx.send('Mods usage:')


@bot.command(aliases=['backup'])
async def save(ctx):
    # TODO: take server name as argument
    src = f'{DST_DIR}/Cluster_5'
    server_name = 'the rust buster'

    dest = f'{BACKUP_DIR}/{server_name}/Backup {datetime.now().strftime("%b-%d-%y %H%M")}'
    try:
        shutil.copytree(src, dest)
        await ctx.send('Server saved!')
        print(f'Server saved to {dest}')

    except Exception as e:
        await ctx.send('Backup failed :( Check console for error')
        print(e)


bot.run(TOKEN)
