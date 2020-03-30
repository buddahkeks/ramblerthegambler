import discord, json, asyncio
from discord.ext import commands

from lib.roulette.roulette import Roulette
from lib.roulette.player import RoulettePlayer

with open('conf.json', 'r') as f:
    conf = json.load(f)

bot = commands.Bot(command_prefix=conf['prefix'])
channel = None
players = dict()
game = Roulette()

async def game_loop():
    while not bot.is_closed():
        game.new_round()
        msg = await channel.send('New game starting in {} seconds'.format(conf['timeout']))
        await asyncio.sleep(conf['timeout']-10)
        for i in range(1,11)[::-1]:
            await msg.edit(content='New game starting in {} seconds'.format(i))
            await asyncio.sleep(1)
        await channel.delete_messages([msg])
        await channel.send('New game has started!')
        res, diff = game.start_round()
        await channel.send('Current result: ' + str(res))
        await channel.send('Differences: ')
        for u, d in diff:
            await channel.send('"{}" --> {}'.format(u, d))

@bot.command()
async def join(ctx):
    if ctx.message.channel != channel:
        return
    if not ctx.message.author.id in players.keys():
        players[ctx.message.author.id] = RoulettePlayer(ctx.author.name, 100)
        game.join(players[ctx.message.author.id])
        await ctx.message.channel.send('Welcome to the game {}!'.format(ctx.message.author.mention))

@bot.command()
async def bet(ctx):
    if ctx.message.channel != channel:
        return
    if not ctx.message.author.id in players.keys():
        join(ctx)
        # bet(ctx)
        # await ctx.message.channel.send('Please join the game first, {}!'.format(ctx.message.author.mention))
        # return
    try:
        game.bet(players[ctx.message.author.id], ' '.join(ctx.message.content.split(' ')[1:]))
    except Exception as e:
        await ctx.message.channel.send('{}: {}'.format(ctx.message.author.mention, str(e)))

@bot.command()
async def listplayers(ctx):
    if ctx.message.channel != channel:
        return
    await ctx.message.channel.send('Players: \n - ')
    await ctx.message.channel.send('\n - '.join(game.bets.keys()))

@bot.command()
async def report(ctx):
    mentions = ctx.message.mentions
    if not mentions:
        await ctx.message.channel.send('Usage: >report [playername], {}!'.format(ctx.message.author.mention))
    elif len(mentions)>1:
        await ctx.message.channel.send('To many arguments! Usage: >report [playername], {}!'.format(ctx.message.author.mention))
    else:
        await ctx.message.channel.send('Sorry. No cheaters, no report system. Please contact our system administrators {}!'.format(ctx.message.author.mention))

# @bot.command()
# async def help(ctx):
#     await ctx.message.channel.send('This is an uncomplete Help-Message. Have a great day, {}!\n>join ... Join the game\n>bet ... Bet on something. Idk. Mätsy should do this'.format(ctx.message.author.mention))

@bot.command()
async def top(ctx):
    await ctx.message.channel.send('Top 10 players:')

@bot.event
async def on_ready():
    global channel
    print('[{}#{}]: Ready ... '.format(bot.user.name, bot.user.discriminator))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='🤑💲CASINO LIFE💲🤑'))
    channel = bot.get_channel(conf['channel'])
    asyncio.ensure_future(game_loop())

def main():
    bot.run(conf['token'])

if __name__ == '__main__':
    main()