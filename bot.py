import asyncio
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.linear_model import LinearRegression
import wolframalpha
import yaml

import discord
from discord.ext import commands

with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

bot = commands.Bot(command_prefix = config['prefix'])

@bot.command()
async def linreg(ctx):
    sender = ctx.author
    channel = ctx.channel
    await ctx.send("Please enter your x values:")
    def check(m):
        return m.author == sender and m.channel == channel
    try:
        xvalues = await bot.wait_for(event = 'message', check = check, timeout = 15)
        xvalues = xvalues.content
    except asyncio.TimeoutError:
        await ctx.send("Time ran out")
    else:
        await ctx.send("Please enter your y values:")
        try:
            yvalues = await bot.wait_for(event = 'message', check = check, timeout = 15)
            yvalues = yvalues.content
        except asyncio.TimeoutError:
            await ctx.send("Time ran out")
    await ctx.send(f'x-values: {xvalues}')
    await ctx.send(f'y-values: {yvalues}')
    xlist = [[float(i) for i in re.findall(r"[-+]?\d*\.\d+|\d+", xvalues)]]
    ylist = [[float(i) for i in re.findall(r"[-+]?\d*\.\d+|\d+", yvalues)]]
    X = np.array(xlist)
    y = np.array(ylist)
    regressor = LinearRegression().fit(X, y)
    formula = f'y = {regressor.coef_[0]}x + {regressor.intercept_}'
    plt.scatter(X, y, color = 'red')
    plt.plot(X, regressor.predict(X), color = 'black', linewidth = 3, label = formula)
    plt.title("Linear Regression")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(loc = 'upper left')
    plt.savefig('temp.png')
    await ctx.send(file = discord.File('temp.png'))

@bot.command(aliases = ['wolfram'])
async def wolframalphasearch(ctx, *, query):
    client = wolframalpha.Client('86RUL9-5X3JUHAKR5')
    results = client.query(query)
    embed = discord.Embed(
        title = f'Wolfram | Alpha results for: {query}',
        description = next(results.results).text
    )
    embed.set_author(
        name = bot.user.name,
        url = 'https://github.com/A1phyte/SufficientlyMathematical',
        icon_url = bot.user.avatar_url
    )
    await ctx.send(embed = embed)



        
bot.run(config['token'])