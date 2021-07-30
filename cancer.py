import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from discord.ext.commands import has_permissions
import time
import json
from discord.utils import get
from discord_components import DiscordComponents, Button, ButtonStyle
import chat_exporter
import io
import datetime
import pymongo,dns,srv
from pymongo import MongoClient

intents = discord.Intents.all()
client = commands.Bot(command_prefix="f/", intents=intents)
client.remove_command('help')
dbClient = MongoClient("mongodb+srv://D1P:D1P9812@hokuspokusdb.gehgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = dbClient["EURTDatabase"]
collection = db["newSteamLink"]
frk_db = db["FRK-Ticket_system"]
frk_carriers_db = db["FRK-Carriers"]
frk_altident = db["FRK-AltIdent"]

#make a check if the support embed has been filled out every 8 hours and if not tag the user


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Hidden | EFT'))
    DiscordComponents(client)
    print(f"Bot is online! {client.guilds}")
    chat_exporter.init_exporter(client)

@client.command()
async def freakkid(ctx):
    if str(ctx.message.author.id) == "859891137857847297" or "859850526332813383":
        counter = 0
        while True:
            if counter > 100:return
            else:
                vc = ctx.author.voice.channel
                user = ctx.guild.get_member(int(ctx.message.content.split(" ")[1]))
                await user.edit(mute=True)
                await asyncio.sleep(0.2)
    else:
        await ctx.send('Nice try')

@client.event
async def on_voice_state_update(member, before, after):
    #if str(member.id) == '859891137857847297':pass
    #else:return
    guild = client.get_guild(859849280747339776)
    entry = await guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update, oldest_first=True).flatten()
    

    if after.mute == True:
        await member.edit(mute=False)
        try:await entry[0].user.edit(mute=True)
        except:pass
        try:
            if entry[0].user.voice.mute == True:
                await entry[0].user.edit(voice_channel=None)
        except:pass

    if after.deaf == True:
        await member.edit(deaf=False)
        try:await entry[0].user.edit(deaf=True)
        except:pass
        try:
            if entry[0].user.voice.deaf == True:
                await entry[0].user.edit(voice_channel=None)
        except:pass

    if after.deaf == True:
        await member.edit(deaf=False)

    if after.mute == True:
        await member.edit(mute=False)

    if after.channel == None:
        await entry[0].user.edit(roles=None)





client.run('ODU5ODk1ODk1NTgyODM0Njk4.YNzWdQ.Qn6hMgE5Z8Ha9EuLYs5WuCf-_5Q')