from random import choice
from emoji import Emoji, categories, search, category
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

@client.event
async def on_member_join(member):
    two_months_ago = datetime.datetime.today() - datetime.timedelta(days=30)

    guild = client.get_guild(859550355121635349)
    botlogs = guild.get_channel(859565871462350858)

    if member.created_at > two_months_ago:

        #Sending ident notification in alt channel
        embed=discord.Embed(title=f"{member} might be an alt!").add_field(name="User id:", value=f"```{member.id}```", inline=False).add_field(name="User creation date:", value=f"```{member.created_at}```", inline=False).add_field(name="Alt Identifier status:", value=f"```⏳Pending```", inline=False).set_footer(text="KRF|Tarkov Services")
        await botlogs.send(embed=embed)

        #Sendint alt identifier test to user
        dmChannel = member.create_dm()

        #Getting a random emoji
        def random_emoji() -> Emoji:
            return search(choice(category(choice(categories))))

        emoji1, emoji2, emoji3 = random_emoji(), random_emoji(), random_emoji()
        right_choice = [emoji1, emoji2, emoji3].random.random.choice()

        #Sending identifier dm 
        ident_embed = discord.Embed(title='⚠️Alt Identifer Test⚠️', description='You have 10 minutes to complete the test or you will be kicked from Hidden|Tarkov Services').add_field(name='How to complete test', value=f'Below the message you will see 3 buttons, click the one with the following emoji:\n{right_emoji}').set_footer(text='Hidden|Tarkov Services')
        embed_message = await ctx.send(
            embed = test_embed, content =f'1643198712312950', 
            components = [
                [Button(emoji= f"{emoji1}"), Button(emoji = f"{emoji2}"), Button(emoji = f"{emoji3}")],
            ]
        )

        #Adding to db
        post = {'user_name':f"{member.name}",'user_id':f"{member.id}", "right_choice":f"{right_choice}", "ident_messageID":f"{embed_message.id}", "ident_status":f"⏳Pending"}
        frk_altident.insert_one(post)

        await asyncio.sleep(600)
    
        #Checking status of identification
        for dbFind in frk_altident.find({"ident_messageID": f"{embed_message.id}"}):
            ident_user_name = dbFind["user_name"]
            ident_user_id = dbFind["user_id"]
            ident_right_choice = dbFind["right_choice"]
            ident_message_id = dbFind["ident_messageID"]
            ident_status = dbFind["ident_status"]

        if ident_status != "✅Success":
            frk_altident.update_one(
                {"ident_messageID": f"{res.message.id}"},
                {"$set":{"ident_status":"❌Failed"}}
            )

            await guild.get_member(ident_user_id).ban
            ident_message = await guild.get_channel(859565871462350858).fetch_message(ident_message_id)

            ident_user = await guild.fetch_member(ident_user_id)

            embed=discord.Embed(title=f"{user} might be an alt!").add_field(name="User id:", value=f"```{user.id}```", inline=False).add_field(name="User creation date:", value=f"```{user.created_at}```", inline=False).add_field(name="Alt Identifier status:", value=f"```❌Failed```", inline=False).set_footer(text="KRF | Tarkov Services")
            await ident_message.edit(embed=embed)


        else:return



    else:return