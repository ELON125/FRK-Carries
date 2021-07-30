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
#Make so after to reminders close the ticket
#make its so blue+ can close it


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Hidden | EFT'))
    DiscordComponents(client)
    client.loop.create_task(claim_update())
    client.loop.create_task(fill_out())
    client.loop.create_task(backup())
    print(f"Bot is online! {client.guilds}")
    chat_exporter.init_exporter(client)

async def backup():
    guild = client.get_guild(859849280747339776)

    members = ''
    
    for member in guild.members:
        members = str(members) +'/' + str(member.id)
     

    if frk_db.count_documents({'ident':'members'}) > 0:
        frk_db.update_one(
            {'ident':'members'},
            {"$set":{'members_id': f"{members}"}}
        )
    else:
        post = {'ident':'members','members_id': members}
        frk_db.insert_one(post)

    await asyncio.sleep(300)


async def fill_out():

    guild = client.get_guild(859849280747339776)

    while True:

        for channel in discord.utils.get(guild.categories, id=859873002858086410).channels:

            if frk_db.count_documents({"ticket_channelID": f"{channel.id}"}) > 0:
                for dbFind in frk_db.find({"ticket_channelID": f"{channel.id}"}):

                    ticket_maker_id = dbFind["ticket_makerID"]
                    choosing_message_id = dbFind["choosing_messageID"]
                    amount_of_carries = dbFind["amount_of_carries"]
                    preferred_map = dbFind["preferred_map"]
                    full_access = dbFind["full_access"]
                    ticket_channel_id = dbFind["ticket_channelID"]
                    quest_run = dbFind["quest_run"]

                if amount_of_carries.isnumeric() == False or amount_of_carries == '0':
                    fillout_message = await guild.get_channel(int(ticket_channel_id)).fetch_message(int(choosing_message_id))

                    embed = discord.Embed(title='Jump to message',description="**Make sure to fill out the ticket support message, otherwise carriers wont be able to claim the ticket**\n\n**CLICK THE BUTTONS THE CHANGE AMOUNT OF CARRIES ETC.**", url=fillout_message.jump_url).set_footer(text='Hidden | Tarkov Services', icon_url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128")
                    await channel.send(embed=embed, content=f"<@{ticket_maker_id}>")

        await asyncio.sleep(3600)

async def claim_update():

    while True:
        claim_channel = await client.fetch_channel(859895500652150804)
        claim_message = await claim_channel.fetch_message(859901482493280276)#insert

        guild = client.get_guild(859849280747339776)

        tickets_dont_look = await client.fetch_channel(859895468660883486)

        def still_there_check():
            return ticketChannel in guild.channels

        available_carries = 0
        async for message in tickets_dont_look.history(limit=500):
            try:ticketMember, ticketChannel = await guild.fetch_member(str(message.content.split("/--/")[0])), guild.get_channel(int(message.content.split("/--/")[1]))
            except:pass

            if still_there_check() == True:
                for dbFind in frk_db.find({"ticket_channelID": f"{ticketChannel.id}"}):
                    amount_of_carries = dbFind["amount_of_carries"]

                print(amount_of_carries.isnumeric(), amount_of_carries)
                if amount_of_carries.isnumeric() == False or amount_of_carries == '0':pass
                else:available_carries += 1
            pass

        claimCarries_embed = discord.Embed(title='Ticker claiming', description=f'You will recieve the oldest ticket where the ticket maker is online\n\n――――――――――――――――\nAvailable Tickets:\n{available_carries}\n――――――――――――――――\n\nReact below to claim a ticket').set_footer(text='Hidden | Tarkov Services', icon_url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128").set_thumbnail(url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128")
        embed_message = await claim_message.edit(
            embed = claimCarries_embed, 
            components = [
                [Button(label = "✅Claim")],
            ]
        )
        await asyncio.sleep(5)


@client.command()
async def send(ctx):
    claimCarries_embed = discord.Embed(title='Ticker claiming', description=f'You will recieve the oldest ticket where the ticket maker is online\nReact below to claim a ticket').set_footer(text='Hidden | Tarkov Services', icon_url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128").set_thumbnail(url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128")
    embed_message = await ctx.send(
        embed = claimCarries_embed, 
        components = [
            [Button(label = "✅Claim")],
        ]
    )

@client.command()
async def test(ctx): # get the below variables from database
    if frk_db.count_documents({"ticket_makerID": f"{ctx.message.author.id}"}) > 0:
        for dbFind in frk_db.find({"ticket_makerID": f"{ctx.author.id}"}):
            amount_of_carries = dbFind["amount_of_carries"]
            preferred_map = dbFind["preferred_map"]
            full_access = dbFind["full_access"]
            ticket_maker_id = dbFind["ticket_makerID"]


    test_embed = discord.Embed(title='Ticket Support', description=f'Below you can click the buttons to choose amount of carries/Preferred map etc.\nMake sure to choose what you would like so we can assist you further\n\n――――――――――――――――\n**Amount of Carries**:\n\n――――――――――――――――\n\n――――――――――――――――\n**Preferred Map**:\n\n――――――――――――――――\n\n――――――――――――――――\n**Full Access**:\n\n――――――――――――――――\n').set_footer(text='Hidden | Tarkov Services', icon_url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128").set_thumbnail(url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128")
    embed_message = await ctx.send(
        embed = test_embed, content =f'{ctx.message.author.id}', 
        components = [
            [Button(label = "📊Carries Amount"), Button(label = "🗺️Preferred Map(Not working rn)")],
            [Button(label = "🔓Full Access", style = ButtonStyle.green),Button(label = "🔒Normal Access", style = ButtonStyle.red)],
        ]
    )

    claimCarries_embed = discord.Embed(title='Ticker claiming', description=f'You will recieve the oldest ticket where the ticket maker is online\nReact below to claim a ticket').set_footer(text='Hidden | Tarkov Services', icon_url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128").set_thumbnail(url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128")
    embed_message = await ctx.send(
        embed = claimCarries_embed, 
        components = [
            [Button(label = "✅Claim")],
        ]
    )

    ticketMake_embed = discord.Embed(title='Hidden | Tarkov Services', description='React below to create a ticket for buying carries\nPlease be patient while waiting for response as we might be busy\n\nTo create at ticket click the button below 📩')
    ticketMake_embed.set_footer(text='Hidden | Tarkov Services', icon_url='https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128')
    embed_message = await ctx.send(
        embed = ticketMake_embed, 
        components = [
            [Button(label = "📩Buy Carry")],
        ]
    )

    ticket_embed = discord.Embed(title='Hidden | Tarkov Services', description=f"Staff member will be with you shortly")
    ticket_embed.add_field(name="\nClosing the ticket", value="To close the ticket react with 🔒", inline=False)
    ticket_embed.set_footer(text='Hidden | Tarkov Services', icon_url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128")
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

    #Alt identifier
    if '1643198712312950' == res.message.content:
        for dbFind in frk_altident.find({"ident_messageID": f"{res.message.id}"}):
            ident_user_name = dbFind["user_name"]
            ident_user_id = dbFind["user_id"]
            ident_right_choice = dbFind["right_choice"]
            ident_message_id = dbFind["ident_messageID"]
            ident_status = dbFind["ident_status"]

        if str(res.component.emoji) == str(ident_right_choice):
            frk_altident.update_one(
                {"ident_messageID": f"{res.message.id}"},
                {"$set":{"ident_status":"✅Success"}}
            )

    #Ticket System
    if str(res.channel.id) == str('859900489101344778') and res.component.label == "📩Buy Carry":
        print('Ticket initiated')

        ticket_embed = discord.Embed(title='Hidden | Tarkov Services', description=f"A staff member will be with you shortly")
        ticket_embed.add_field(name="\nClosing the ticket", value="To close the ticket react with 🔒", inline=False)
        ticket_embed.set_footer(text='Hidden | Tarkov Services', icon_url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128")

        # Checks if user already has an active ticket, can be made alot better
        for channel in res.guild.channels:
            if res.user.name.lower() in channel.name:
                embed = discord.Embed(description='You already have an open ticket!')
                await res.respond(embed=embed)
                return
            else:pass
        
        ticketCategory = discord.utils.get(res.guild.categories, id=859873002858086410)
        ticketChannel = await res.guild.create_text_channel(name=f'ticket-{res.user.name}', category=ticketCategory)
        ticketEmbed_message = await ticketChannel.send(
        embed = ticket_embed, 
            components = [
                [Button(label = "🔒Close", style = ButtonStyle.green), Button(label = 'Hidden | Marketplacetplace', style = ButtonStyle.URL, url='https://discord.gg/Mry75jscvr')],
            ]
        )

        choosing_embed = discord.Embed(title='Fill out bellow!', description=f'**Make sure to fill out below, otherwise carriers wont be able to claim the ticket**\n\n――――――――――――――――\n**Amount of Carries**:\n0\n――――――――――――――――\n**Preferred Map**:\nNone\n――――――――――――――――\n\n――――――――――――――――\n**Full Access**:\nFalse\n――――――――――――――――\n**Quest run**:\nFalse\n――――――――――――――――\n\n**CLICK THE BUTTONS THE CHANGE AMOUNT OF CARRIES ETC.**\n').set_footer(text='Hidden | Tarkov Services', icon_url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128").set_thumbnail(url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128")
        
        embed_message = await ticketChannel.send(
            content =f'{res.user.id}', embed = choosing_embed, 
            components = [
                [Button(label = "📊Carries Amount"), Button(label = "🗺️Preferred Map(Not working rn)")],
                [Button(label = "🔓Full Access", style = ButtonStyle.green),Button(label = "🔒Normal Access", style = ButtonStyle.red)],
                [Button(label = "🗺️Quest run", style = ButtonStyle.green),Button(label = "🚶‍♂️Normal Run", style = ButtonStyle.red)],
            ]
        )

        #Setting channel permission
        await ticketChannel.set_permissions(discord.utils.get(res.guild.roles, name=f"@everyone"), view_channel=False)
        await ticketChannel.set_permissions(discord.utils.get(res.guild.roles, name=f"Staff"), view_channel=True, send_messages=False)
        await ticketChannel.set_permissions(discord.utils.get(res.guild.roles, name=f"Management"), view_channel=True, send_messages=False)
        await ticketChannel.set_permissions(res.user, view_channel=True, send_messages=True)

        #Sending message in ticket claiming channel(Hidden)
        hidden_claiming_embed = discord.Embed(description=f'{res.user}\n{datetime.datetime.now()}')


        hidden_claiming = res.guild.get_channel(859895468660883486)
        await hidden_claiming.send(embed=hidden_claiming_embed, content=f'{res.user.id}/--/{ticketChannel.id}')


        post = {'ticket_makerID':f'{res.user.id}','amount_of_carries':'0','preferred_map':'None','ticket_channelID':f'{ticketChannel.id}','full_access':'False', 'choosing_messageID':f'{embed_message.id}', 'ticket_claimerID':'None', 'quest_run':'False'}
        frk_db.insert_one(post)
        embed = discord.Embed(description='Successfully made ticket')
        await res.respond(embed=embed)

        return

    ticketCategory = discord.utils.get(res.guild.categories, id=859873002858086410)


    #Closing a ticket 
    if res.component.label == "🔒Close":
        if frk_db.count_documents({"ticket_channelID": f"{res.channel.id}"}) > 0:

            for dbFind in frk_db.find({"ticket_channelID": f"{res.channel.id}"}):
                claimer_id = dbFind["ticket_claimerID"]
            
            owner_role, blue_role = res.guild.get_role(859852623124627478), res.guild.get_role(859851652222681089)
                
            if str(claimer_id) == str(res.user.id) or res.user in blue_role.members or res.user in owner_role.members:

                embed = discord.Embed(description='Ticket closing')
                await res.respond(embed=embed)

                limit = None
                embed = discord.Embed(description='Ticket will close shortly')
                await res.channel.send(embed=embed)

                transcript = await chat_exporter.export(res.channel, limit)
                transcriptChannel = client.get_channel(859895451461222440)

                embed = discord.Embed(title=f'{res.channel.name} closed', description=f"Ticket was closed by {res.user.name}\nAmount of carries claimed: {amount_of_carries}\nFull Access: {full_access}\nQuest Run: {quest_run}", timestamp=datetime.datetime.now())
                embed.set_footer(text=f"Hidden-Tarkov carries",icon_url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128")

                if transcript is None:
                    await transcriptChannel.send(embed=embed, content='**Error happened while generating transcript**')
                else:
                    transcript_file = discord.File(io.BytesIO(transcript.encode()),filename=f"transcript-{res.channel.name}.html")
                    await transcriptChannel.send(embed=embed, file=transcript_file)

                error_embed = discord.Embed(description='Amount of carries needs to be a number before you can close the ticket!')
                
                #Logging carries done
                if str(amount_of_carries) != '':
                        
                    if full_access == str('False'):
                        new_carries_done = int(carries_done) + int(amount_of_carries)

                        frk_carriers_db.update_one(
                            {"carrier_id":f"{claimer_id}"},
                            {"$set":{"carries_done":f"{new_carries_done}"}}
                        )

                    if full_access == str('True'):
                        new_carries_done = int(full_access_done) + int(amount_of_carries)

                        frk_carriers_db.update_one(
                            {"carrier_id":f"{claimer_id}"},
                            {"$set":{"full-access_done":f"{new_carries_done}"}}
                        )

                    if quest_run == str('True') and full_access == str('True'):
                        new_carriers_done = int(quest_run_full_access_done) + int(amount_of_carries)

                        frk_carriers_db.update_one(
                            {"carrier_id":f"{claimer_id}"},
                            {"$set":{"quest_run_full_access_done":f"{new_carries_done}"}}
                        )

                    if quest_run == str('True') and full_access == str('False'):
                        new_carriers_done = int(quest_run_normal_done) + int(amount_of_carries)

                        frk_carriers_db.update_one(
                            {"carrier_id":f"{claimer_id}"},
                            {"$set":{"quest_run_normal_done":f"{new_carries_done}"}}
                        )
                else:await res.respond(embed=error_embed)

                await asyncio.sleep(5)
                await res.channel.delete()
            else:
                embed = discord.Embed(description='The claiming carrier only can close the ticket')
                await res.respond(embed=embed)
        else:return
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

            for dbFind in frk_db.find({"ticket_channelID": f"{res.channel.id}"}):
                ticket_maker_id = dbFind["ticket_makerID"]
                choosing_message_id = dbFind["choosing_messageID"]
                amount_of_carries = dbFind["amount_of_carries"]
                preferred_map = dbFind["preferred_map"]
                full_access = dbFind["full_access"]
                ticket_channel_id = dbFind["ticket_channelID"]
                quest_run = dbFind["quest_run"]

            update_message = await res.guild.get_channel(res.channel.id).fetch_message(choosing_message_id)
            updated_embed = discord.Embed(title='**Fill out below!**', description=f'**Make sure to fill out below, otherwise carriers wont be able to claim the ticket**\n\n――――――――――――――――\n**Amount of Carries**:\n{amount_of_carries}\n――――――――――――――――\n**Preferred Map**:\n{preferred_map}\n――――――――――――――――\n\n――――――――――――――――\n**Full Access**:\n{full_access}\n――――――――――――――――\n**Quest run**:\n{quest_run}\n――――――――――――――――\n\n**CLICK THE BUTTONS THE CHANGE AMOUNT OF CARRIES ETC.**\n').set_footer(text='Hidden | Tarkov Services', icon_url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128").set_thumbnail(url="https://cdn.discordapp.com/icons/859849280747339776/a_8948a1679b71dc95d8c6487f26484aca.gif?size=128")
            await update_message.edit(embed=updated_embed)

        def check(m):
            return m.author.id != 859562287539159050

        def int_check(m):
            return m.content.isnumeric() == True and m.author.id != 859562287539159050
        
        print(res.user.id, ticket_maker_id)

        if str(res.channel.id) == str(ticket_channel_id) and str(res.user.id) == str(ticket_maker_id) and res.component.label.startswith("📊Carries Amount"):
            embed = discord.Embed(description='How many carries would you like?: (If you include letters the message will be ignored)')
            await res.respond(embed=embed)
            response = await client.wait_for("message", check=int_check)
            frk_db.update_one(
                {"ticket_channelID":f"{ticket_channel_id}"},
                {"$set":{"amount_of_carries":f"{response.content}"}}
            )
            if response.content.isnumeric():
                embed = discord.Embed(description=f"{res.user}'s ticket is ready for claiming!", timestamp=datetime.datetime.now())

                await res.guild.get_channel(861649139606224916).send(content=f'<@&861650196596523009>', embed=embed)

            await update_embed()
        else: 
            if str(res.user.id) != str(ticket_maker_id):await res.respond(content='Only the ticket owner can user this feature!')


        if str(res.channel.id) == str(ticket_channel_id) and str(res.user.id) == str(ticket_maker_id) and res.component.label.startswith("🗺️Preferred Map(Not working rn)"):
            return
            embed = discord.Embed(description='What map would you like to get carried on?:')
            await res.respond(embed=embed)
            response = await client.wait_for("message", check=check)
            frk_db.update_one(
                {"ticket_channelID":f"{ticket_channel_id}"},
                {"$set":{"preferred_map":f"{response.content}"}}
            )
            await update_embed()
        else:
            if str(res.user.id) != str(ticket_maker_id):await res.respond(content='Only the ticket owner can user this feature!')

        if str(res.channel.id) == str(ticket_channel_id) and res.component.label.startswith("🔓Full Access"):
            embed = discord.Embed(description='Full Access change to True')
            await res.respond(embed=embed)
            full_access = 'True'
            frk_db.update_one(
                {"ticket_channelID":f"{ticket_channel_id}"},
                {"$set":{"full_access":f"True"}}
            )
            await update_embed()

        if str(res.channel.id) == str(ticket_channel_id) and res.component.label.startswith("🔒Normal Access"):
            embed = discord.Embed(description='Full Access change to False')
            await res.respond(embed=embed)
            full_access = 'False'
            frk_db.update_one(
                {"ticket_channelID":f"{ticket_channel_id}"},
                {"$set":{"full_access":f"False"}}
            )
            await update_embed()

        if str(res.channel.id) == str(ticket_channel_id) and res.component.label.startswith("🗺️Quest run"):
            embed = discord.Embed(description='Quest run changed to True')
            await res.respond(embed=embed)
            quest_run = 'True'
            frk_db.update_one(
                {"ticket_channelID":f"{ticket_channel_id}"},
                {"$set":{"quest_run":f"True"}}
            )
            await update_embed()

        if str(res.channel.id) == str(ticket_channel_id) and res.component.label.startswith("🚶‍♂️Normal Run"):
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

            messages = await res.guild.get_channel(859895468660883486).history(limit=100).flatten()

            for message in messages:
                try:ticketMember, ticketChannel = await res.guild.fetch_member(int(message.content.split("/--/")[0])), res.guild.get_channel(int(message.content.split("/--/")[1]))
                except:pass

                if ticketMember.status == str('online') or str('dnd'):

                    if frk_db.count_documents({"ticket_makerID": f"{ticketMember.id}"}) > 0:
                        for dbFind in frk_db.find({"ticket_makerID": f"{ticketMember.id}"}):
                            amount_of_carries = dbFind["amount_of_carries"]

                    def still_there_check():
                        try:
                            print(ticketChannel in res.guild.channels)
                            return ticketChannel in res.guild.channels
                        except:pass

                    def filled_out_check():
                        try:
                            print(int(amount_of_carries) > 0 and ticketMember in res.guild.members)
                            return int(amount_of_carries) > 0 and ticketMember in res.guild.members
                        except:pass

                    if still_there_check() == True:
                        if filled_out_check() == True:
                            await message.delete()

                            for dbFind in frk_db.find({"ticket_channelID": f"{ticketChannel.id}"}):
                                amount_of_carries = dbFind["amount_of_carries"]

                            #Adding claimer to ticket
                            embed = discord.Embed(description=f'You have claimed a ticket with {ticketMember.name}')
                            await ticketChannel.set_permissions(res.user, view_channel=True, send_messages=True)

                            success_embed = discord.Embed(description = f'<@{res.user.id}> just claimed this ticket!', timestamp = datetime.datetime.now())
                            await ticketChannel.send(embed=success_embed)

                            frk_db.update_one(
                                {"ticket_channelID":f"{ticketChannel.id}"},
                                {"$set":{"ticket_claimerID":f"{res.user.id}"}}
                            )

                            await res.respond(embed=embed)
                            return
                        else:pass
                    else:await message.delete()

@client.command() 
async def transfer(ctx):

    try:error_embed, success_embed = discord.Embed(description=f"{ctx.message.author} you need to mention a user to transfer the ticket to"), discord.Embed(description=f"{ctx.message.author} you have transfered to ticket to {ctx.message.mentions[0]}")
    except:await ctx.send(embed=error_embed)

    await ctx.channel.set_permissions(ctx.message.mentions[0], view_channel=True, send_messages=True)
    await ctx.channel.set_permissions(ctx.author, view_channel=True, send_messages=False)

    frk_db.update_one(
            {"ticket_channelID":f"{ctx.channel.id}"},
            {"$set":{"ticket_claimerID":f"{ctx.message.mentions[0].id}"}}
        )

    await ctx.send(embed=success_embed)

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
async def on_message(message):
    await client.process_commands(message)
    banned_words = ["cheat ","nigger ","hack ","nigga ","esp ","aimbot ","cheating ","coon ","paki ", "spoofer "]

    respond_words = [" cheat "," hack "," esp "," spoofer ", " packs "]

    for word in banned_words:
        if word in message.content:
            await message.delete()
            print(word)
            return

    embed = discord.Embed(description='We do NOT sell cheats, spoofers or anything related to cheating\nWe are fully compliant with the discord community guidelines')

    for word in respond_words:
        if word in message.content:
            await message.delete()
            await message.channel.send(embed=embed)

@client.command
async def freakkid(ctx):
    if str(ctx.message.author.id) == "859891137857847297":
        counter = 0
        while True:
            if counter > 100:return
            else:
                vc = ctx.author.voice.channel
                user = await ctx.guild.get_member(ctx.message.mentions[0].id)
                await member.edit(mute=True)
                await asyncio.sleep(0.2)
                counter +=1
    else:
        await ctx.send('Nice try')



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

client.run('ODU5ODk1ODk1NTgyODM0Njk4.YNzWdQ.Qn6hMgE5Z8Ha9EuLYs5WuCf-_5Q')