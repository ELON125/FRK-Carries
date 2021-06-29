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
import pymongo,dns
from pymongo import MongoClient

client = commands.Bot(command_prefix="f/")
client.remove_command('help')
dbClient = MongoClient("mongodb+srv://D1P:D1P9812@hokuspokusdb.gehgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = dbClient["EURTDatabase"]
collection = db["newSteamLink"]
frk_db = db["FRK-Ticket_system"]
frk_carriers_db = db["FRK-Carriers"]

#make a check if the support embed has been filled out every 8 hours and if not tag the user



@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game('FRK | Carries'))
  DiscordComponents(client)
  client.loop.create_task(claim_update())
  print("Bot is online!")

async def fill_out():

    guild = client.get_guild(796445790154653727)

    while True:

        for channel in discord.utils.get(guild.categories, id=844312009972383816).channels:

            if frk_db.count_documents({"ticket_channelID": f"{channel.id}"}) > 0:
                for dbFind in frk_db.find({"ticket_channelID": f"{channel.id}"}):

                    ticket_maker_id = dbFind["ticket_makerID"]
                    choosing_message_id = dbFind["choosing_messageID"]
                    amount_of_carries = dbFind["amount_of_carries"]
                    preferred_map = dbFind["preferred_map"]
                    full_access = dbFind["full_access"]
                    ticket_channel_id = dbFind["ticket_channelID"]
                    quest_run = dbFind["quest_run"]

                if amount_of_carries == '0':
                    fillout_message = await guild.get_channel(int(ticket_channel_id)).fetch_message(int(choosing_message_id))

                    embed = discord.Embed(title='Jump to message',description="⚠️Make sure to fill out the ticket support message, otherwise carriers wont be able to claim the ticket⚠️", url=fillout_message.jump_url)
                    await channel.send(embed=embed, content=f"<@{ticket_maker_id}>")

        await asyncio.sleep(7200)

async def claim_update():

    while True:
        print('Updating')
        claim_channel = await client.fetch_channel(859195265978597436)
        claim_message = await claim_channel.fetch_message(859205471498666054)

        tickets_dont_look = await client.fetch_channel(859195518353539102)

        available_carries = 0
        async for message in tickets_dont_look.history(limit=500):
            available_carries += 1

        claimCarries_embed = discord.Embed(title='Ticker claiming', description=f'You will recieve the oldest ticket where the ticket maker is online\n\n――――――――――――――――\nAvailable Tickets:\n{available_carries}\n――――――――――――――――\n\nReact below to claim a ticket').set_footer(text='FRK Tarkov Carries', icon_url="https://media.discordapp.net/attachments/798922297062850600/800336476826763334/chingyhasasmallcock.gif").set_thumbnail(url="https://cdn.discordapp.com/attachments/781284773083480064/856569431031021598/leems_shit_logo.gif")
        embed_message = await claim_message.edit(
            embed = claimCarries_embed, 
            components = [
                [Button(label = "✅Claim")],
            ]
        )
        await asyncio.sleep(5)

@client.command()
async def test(ctx): # get the below variables from database
    if frk_db.count_documents({"ticket_makerID": f"{ctx.message.author.id}"}) > 0:
        for dbFind in frk_db.find({"ticket_makerID": f"{ctx.author.id}"}):
            amount_of_carries = dbFind["amount_of_carries"]
            preferred_map = dbFind["preferred_map"]
            full_access = dbFind["full_access"]
            ticket_maker_id = dbFind["ticket_makerID"]


    test_embed = discord.Embed(title='Ticket Support', description=f'Below you can click the buttons to choose amount of carries/Preferred map etc.\nMake sure to choose what you would like so we can assist you further\n\n――――――――――――――――\n**Amount of Carries**:\n\n――――――――――――――――\n\n――――――――――――――――\n**Preferred Map**:\n\n――――――――――――――――\n\n――――――――――――――――\n**Full Access**:\n\n――――――――――――――――\n').set_footer(text='FRK Tarkov Carries', icon_url="https://media.discordapp.net/attachments/798922297062850600/800336476826763334/chingyhasasmallcock.gif").set_thumbnail(url="https://cdn.discordapp.com/attachments/781284773083480064/856569431031021598/leems_shit_logo.gif")
    embed_message = await ctx.send(
        embed = test_embed, content =f'{ctx.message.author.id}', 
        components = [
            [Button(label = "📊Carries Amount"), Button(label = "🗺️Preferred Map")],
            [Button(label = "🔓Full Access", style = ButtonStyle.green),Button(label = "🔒Normal Access", style = ButtonStyle.red)],
        ]
    )

    claimCarries_embed = discord.Embed(title='Ticker claiming', description=f'You will recieve the oldest ticket where the ticket maker is online\nReact below to claim a ticket').set_footer(text='FRK Tarkov Carries', icon_url="https://media.discordapp.net/attachments/798922297062850600/800336476826763334/chingyhasasmallcock.gif").set_thumbnail(url="https://cdn.discordapp.com/attachments/781284773083480064/856569431031021598/leems_shit_logo.gif")
    embed_message = await ctx.send(
        embed = claimCarries_embed, 
        components = [
            [Button(label = "✅Claim")],
        ]
    )

    ticketMake_embed = discord.Embed(title='FRK Carries', description='React below to create a ticket for buying carries\nPlease be patient while waiting for response as we might be busy\n\nTo create at ticket click the button below 📩')
    ticketMake_embed.set_footer(text='FRK Tarkov Carries', icon_url='https://cdn.discordapp.com/attachments/781284773083480064/856569431031021598/leems_shit_logo.gif')
    embed_message = await ctx.send(
        embed = ticketMake_embed, 
        components = [
            [Button(label = "📩Buy Carry")],
        ]
    )

    ticket_embed = discord.Embed(title='FRK Carries', description=f"Staff member will be with you shortly")
    ticket_embed.add_field(name="\nClosing the ticket", value="To close the ticket react with 🔒", inline=False)
    ticket_embed.set_footer(text='FRK Tarkov Carries', icon_url="https://media.discordapp.net/attachments/798922297062850600/800336476826763334/chingyhasasmallcock.gif")
    embed_message = await ctx.send(
        embed = ticket_embed, 
        components = [
            [Button(label = "🔒Close", style = ButtonStyle.green), Button(label = '❌Unclaim', style = ButtonStyle.red)],
        ]
    )

@client.command()
async def cinfo(ctx):
    if frk_carriers_db.count_documents({"carrier_id": f"{res.user.id}"}) > 0:
        for dbFind in frk_carriers_db.find({"carrier_id": f"{res.user.id}"}):
            carries_done = dbFind["carries_done"]
            full_access_done = dbFind["full_access_done"]
            quest_run_full_access_done = dbFind["quest_run_full_access_done"]
            quest_run_normal_done = dbFind["quest_run_normal_done"]
    await ctx.send()


@client.event
async def on_button_click(res):

    if frk_db.count_documents({"ticket_channelID": f"{res.channel.id}"}) > 0:
        for dbFind in frk_db.find({"ticket_channelID": f"{res.channel.id}"}):
            ticket_maker_id = dbFind["ticket_makerID"]
            choosing_message_id = dbFind["choosing_messageID"]
            amount_of_carries = dbFind["amount_of_carries"]
            preferred_map = dbFind["preferred_map"]
            full_access = dbFind["full_access"]
            ticket_channel_id = dbFind["ticket_channelID"]
            quest_run = dbFind["quest_run"]

    if frk_carriers_db.count_documents({"carrier_id": f"{res.user.id}"}) > 0:
        for dbFind in frk_carriers_db.find({"carrier_id": f"{res.user.id}"}):
            carries_done = dbFind["carries_done"]
            full_access_done = dbFind["full_access_done"]
            quest_run_full_access_done = dbFind["quest_run_full_access_done"]
            quest_run_normal_done = dbFind["quest_run_normal_done"]

    #Ticket System
    if str(res.channel.id) == str('859195101774086185') and res.component.label == "📩Buy Carry":
        print('Ticket initiated')

        ticket_embed = discord.Embed(title='FRK Carries', description=f"A staff member will be with you shortly")
        ticket_embed.add_field(name="\nClosing the ticket", value="To close the ticket react with 🔒", inline=False)
        ticket_embed.set_footer(text='FRK Tarkov Carries', icon_url="https://media.discordapp.net/attachments/798922297062850600/800336476826763334/chingyhasasmallcock.gif")

        # Checks if user already has an active ticket, can be made alot better
        for channel in res.guild.channels:
            if res.user.name.lower() in channel.name:
                embed = discord.Embed(description='You already have an open ticket!')
                await res.respond(embed=embed)
                return
            else:pass
        
        ticketCategory = discord.utils.get(res.guild.categories, id=844312009972383816)
        ticketChannel = await res.guild.create_text_channel(name=f'ticket-{res.user.name}', category=ticketCategory)
        ticketEmbed_message = await ticketChannel.send(
        embed = ticket_embed, 
            components = [
                [Button(label = "🔒Close", style = ButtonStyle.green), Button(label = 'FRK Marketplace', style = ButtonStyle.URL, url='https://discord.gg/Mry75jscvr')],
            ]
        )

        choosing_embed = discord.Embed(title='Ticket Support', description=f'Below you can click the buttons to choose amount of carries/Preferred map etc.\nMake sure to choose what you would like so we can assist you further\n\n――――――――――――――――\n**Amount of Carries**:\n0\n――――――――――――――――\n**Preferred Map**:\nNone\n――――――――――――――――\n\n――――――――――――――――\n**Full Access**:\nFalse\n――――――――――――――――\n**Quest run**:\nFalse\n――――――――――――――――\n').set_footer(text='FRK Tarkov Carries', icon_url="https://media.discordapp.net/attachments/798922297062850600/800336476826763334/chingyhasasmallcock.gif").set_thumbnail(url="https://cdn.discordapp.com/attachments/781284773083480064/856569431031021598/leems_shit_logo.gif")
        
        embed_message = await ticketChannel.send(
            content =f'{res.user.id}', embed = choosing_embed, 
            components = [
                [Button(label = "📊Carries Amount"), Button(label = "🗺️Preferred Map")],
                [Button(label = "🔓Full Access", style = ButtonStyle.green),Button(label = "🔒Normal Access", style = ButtonStyle.red)],
                [Button(label = "🗺️Quest run", style = ButtonStyle.green),Button(label = "🚶‍♂️Normal Run", style = ButtonStyle.red)],
            ]
        )

        await ticketChannel.set_permissions(discord.utils.get(res.guild.roles, name=f"@everyone"), view_channel=False)
        await ticketChannel.set_permissions(res.user, view_channel=True)

        #Sending message in ticket claiming channel(Hidden)
        hidden_claiming_embed = discord.Embed(description=f'{res.user}\n{datetime.datetime.now()}')


        hidden_claiming = res.guild.get_channel(859195518353539102)
        await hidden_claiming.send(embed=hidden_claiming_embed, content=f'{res.user.id}/--/{ticketChannel.id}')


        post = {'ticket_makerID':f'{res.user.id}','amount_of_carries':'0','preferred_map':'None','ticket_channelID':f'{ticketChannel.id}','full_access':'False', 'choosing_messageID':f'{embed_message.id}', 'ticket_claimerID':'None', 'quest_run':'False'}
        frk_db.insert_one(post)
        embed = discord.Embed(description='Successfully made ticket')
        await res.respond(embed=embed)
        return

    ticketCategory = discord.utils.get(res.guild.categories, id=844312009972383816)


    #Closing a ticket 
    if res.component.label == "🔒Close":
        embed = discord.Embed(description='Ticket closing...')
        await res.respond(embed=embed)

        limit = None
        embed = discord.Embed(description='Ticket will close shortly')
        await res.channel.send(embed=embed)

        transcript = await chat_exporter.export(res.channel, limit)
        transcript_file = discord.File(io.BytesIO(transcript.encode()),filename=f"transcript-{res.channel.name}.html")
        transcriptChannel = client.get_channel(844260771558850631)

        embed = discord.Embed(title=f'{res.channel.name} closed', description=f"Ticket was closed by {res.user.name}", timestamp=datetime.datetime.now())
        embed.set_footer(text=f"FRK-Tarkov carries",icon_url="https://media.discordapp.net/attachments/798922297062850600/800336476826763334/chingyhasasmallcock.gif")

        await transcriptChannel.send(embed=embed, file=transcript_file)
        
        #Logging carries done
                
        if full_access == str('False'):
            new_carries_done = int(carries_done) + int(amount_of_carries)

            frk_carriers_db.update_one(
                {"carrier_id":f"{res.user.id}"},
                {"$set":{"carries_done":f"{new_carries_done}"}}
            )

        if full_access == str('True'):
            new_carries_done = int(full_access_done) + int(amount_of_carries)

            frk_carriers_db.update_one(
                {"carrier_id":f"{res.user.id}"},
                {"$set":{"full-access_done":f"{new_carries_done}"}}
            )

        if quest_run == str('True') and full_access == str('True'):
            new_carriers_done = int(quest_run_full_access_done) + int(amount_of_carries)

            frk_carriers_db.update_one(
                {"carrier_id":f"{res.user.id}"},
                {"$set":{"quest_run_full_access_done":f"{new_carries_done}"}}
            )

        if quest_run == str('True') and full_access == str('False'):
            new_carriers_done = int(quest_run_normal_done) + int(amount_of_carries)

            frk_carriers_db.update_one(
                {"carrier_id":f"{res.user.id}"},
                {"$set":{"quest_run_normal_done":f"{new_carries_done}"}}
            )

        await asyncio.sleep(5)
        await res.channel.delete()

    #Unclaiming tickets

    if res.component.label == '#❌Unclaim': # Remove # to make command work but its not needed rn

        embed = discord.Embed(description='Unclaiming ticket now...')
        await res.respond(embed=embed)

        for message in await res.channel.history(limit=100).flatten():
            if message.author.id == res.user.id:await message.delete()
            else:pass

        await res.channel.set_permissions(discord.utils.get(res.guild.roles, name=f"🔐 Carrier"), view_channel=False)

        frk_db.update_one(
                {"ticket_channelID":f"859200634695057418"},
                {"$set":{"ticket_claimerID":"None"}}
            )

    #Carry amount choosing
    if res.channel.name.startswith("ticket-"):

        async def update_embed():
            update_message = await res.guild.get_channel(res.channel.id).fetch_message(choosing_message_id)
            updated_embed = discord.Embed(title='Ticket Support', description=f'Below you can click the buttons to choose amount of carries/Preferred map etc.\nMake sure to choose what you would like so we can assist you further\n\n――――――――――――――――\n**Amount of Carries**:\n{amount_of_carries}\n――――――――――――――――\n**Preferred Map**:\n{preferred_map}\n――――――――――――――――\n\n――――――――――――――――\n**Full Access**:\n{full_access}\n――――――――――――――――\n**Quest run**:\n{quest_run}\n――――――――――――――――\n').set_footer(text='FRK Tarkov Carries', icon_url="https://media.discordapp.net/attachments/798922297062850600/800336476826763334/chingyhasasmallcock.gif").set_thumbnail(url="https://cdn.discordapp.com/attachments/781284773083480064/856569431031021598/leems_shit_logo.gif")
            await update_message.edit(embed=updated_embed)

        async def check(m):
            return m.author.id == ticket_maker_id 

        async def int_check(m):
            a_string = m.content
            a_string_lowercase = a_string.lower()
            contains_letters = a_string_lowercase.islower()	
            return m.author.id == ticket_maker_id and contains_letters == False

        if str(res.channel.id) == str(ticket_channel_id) and str(res.user.id) == str(ticket_maker_id) and res.component.label.startswith("📊Carries Amount"):
            embed = discord.Embed(description='How many carries would you like?:')
            await res.respond(embed=embed)
            response = await client.wait_for("message", check=int_check)
            amount_of_carries = response.content
            frk_db.update_one(
                {"ticket_channelID":f"{ticket_channel_id}"},
                {"$set":{"amount_of_carries":f"{response.content}"}}
            )
            await update_embed()

        if str(res.channel.id) == str(ticket_channel_id) and str(res.user.id) == str(ticket_maker_id) and res.component.label.startswith("🗺️Preferred Map"):
            embed = discord.Embed(description='What map would you like to get carried on?:')
            await res.respond(embed=embed)
            response = await client.wait_for("message", check=check)
            preferred_map = response.content
            frk_db.update_one(
                {"ticket_channelID":f"{ticket_channel_id}"},
                {"$set":{"preferred_map":f"{response.content}"}}
            )
            await update_embed()

        if str(res.channel.id) == str(ticket_channel_id) and str(res.user.id) == str(ticket_maker_id) and res.component.label.startswith("🔓Full Access"):
            embed = discord.Embed(description='Full Access change to True')
            await res.respond(embed=embed)
            full_access = 'True'
            frk_db.update_one(
                {"ticket_channelID":f"{ticket_channel_id}"},
                {"$set":{"full_access":f"True"}}
            )
            await update_embed()

        if str(res.channel.id) == str(ticket_channel_id) and str(res.user.id) == str(ticket_maker_id) and res.component.label.startswith("🔒Normal Access"):
            embed = discord.Embed(description='Full Access change to False')
            await res.respond(embed=embed)
            full_access = 'False'
            frk_db.update_one(
                {"ticket_channelID":f"{ticket_channel_id}"},
                {"$set":{"full_access":f"False"}}
            )
            await update_embed()

        if str(res.channel.id) == str(ticket_channel_id) and str(res.user.id) == str(ticket_maker_id) and res.component.label.startswith("🗺️Quest run"):
            embed = discord.Embed(description='Quest run changed to True')
            await res.respond(embed=embed)
            quest_run = 'True'
            frk_db.update_one(
                {"ticket_channelID":f"{ticket_channel_id}"},
                {"$set":{"quest_run":f"True"}}
            )
            await update_embed()

        if str(res.channel.id) == str(ticket_channel_id) and str(res.user.id) == str(ticket_maker_id) and res.component.label.startswith("🚶‍♂️Normal Run"):
            embed = discord.Embed(description='Quest run changed to False')
            await res.respond(embed=embed)
            quest_run = 'False'
            frk_db.update_one(
                {"ticket_channelID":f"{ticket_channel_id}"},
                {"$set":{"quest_run":f"False"}}
            )
            await update_embed()

    #Claim carries 
    if res.channel.name.startswith("claim-carry"):
    #When creating a ticket is has to say user_id/--/ticket_channel_id 
        if res.component.label == ("✅Claim"):

            async for message in res.guild.get_channel(859195518353539102).history(limit=100, oldest_first=True):

                ticketMember = await res.guild.fetch_member(str(message.content.split("/--/")[0]))
                ticketChannel = res.guild.get_channel(int(message.content.split("/--/")[1]))

                for dbFind in frk_db.find({"ticket_channelID": f"{ticketChannel.id}"}):
                    amount_of_carries = dbFind["amount_of_carries"]

                if ticketMember.status == str('online') or str('dnd'):

                    def still_there_check():
                        print(ticketChannel in res.guild.channels)
                        return ticketChannel in res.guild.channels

                    def filled_out_check():
                        print(int(amount_of_carries) > 0)
                        return int(amount_of_carries) > 0

                    if still_there_check() == False:
                        if filled_out_check() == True:
                            await message.delete()

                            await ticketChannel.set_permissions(res.user, view_channel=True)
                            embed = discord.Embed(description=f'You have claimed a ticket with {ticketMember.name}')

                            print(ticketChannel.id)
                            frk_db.update_one(
                                {"ticket_channelID":f"{ticketChannel.id}"},
                                {"$set":{"ticket_claimerID":f"{res.user.id}"}}
                            )

                            await res.respond(embed=embed)
                        else:pass
                    else:await message.delete()


@client.command()
async def carrier_add(ctx):
    if frk_carriers_db.count_documents({"carrier_id": f"{ctx.message.mentions[0].id}"}) > 0:

        alreadyCarrier_embed = discord.Embed(description='That user is already in the carrier db')
        await ctx.send(embed=alreadyCarrier_embed)
        return

    else:
        post = {'carrier_id':f'{ctx.message.mentions[0].id}', 'carries_done': '0', 'full_access_done': '0', 'quest_run_full_access_done':'0', 'quest_run_normal_done':'0'}
        frk_carriers_db.insert_one(post)

        carrierAdded_embed = discord.Embed(description='Member has been added to the carrier db')
        await ctx.send(embed=carrierAdded_embed)


@client.event
async def on_raw_reaction_add(payload):

    if payload.member.id == 810906858041770004:
        return

    guild = client.get_guild(payload.guild_id) 
    payloadChannel = guild.get_channel(payload.channel_id)
    payloadMessage = await payloadChannel.fetch_message(payload.message_id)



@client.command()
@commands.has_permissions(ban_members=True, kick_members=True)
async def clear(message, amount = 5):
	await message.channel.purge(limit=amount)

client.run('ODEwOTA2ODU4MDQxNzcwMDA0.YCqd3A.9_027yZ0EJ7QDm4R1YakCzTkMQ0')