import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from discord.ext.commands import has_permissions
import time
import json
from discord.utils import get

client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game('FRK | Carries'))
  print("Bot is online!")

@client.command(name='clear', help='this command will clear msgs')
@commands.has_permissions(ban_members=True, kick_members=True)
async def clear(message, amount = 5):
	member = message.author
	channel2 = await member.create_dm()
	channel = client.get_channel(message.channel.id)
	if message.channel.id == 810910208959840296:
		print('Command stopped!')
		await channel2.send("You cant use the .clear command in this channel!")
	else:
		if message.channel.id == 810910248755789835:
			print('Command stopped! 2')
			await channel.send("You cant use the .clear command in this channel!")
		else:
			await message.channel.purge(limit=amount)

@client.command()
async def embed(ctx):
    embed = discord.Embed(title='FRK Carries', description='React below to create a ticket for buying carries\n Please be patient while waiting for response as we might be busy')
    embed.add_field(name='\u200b', value='To create a ticket react with 📩')
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/798922297062850600/800336476826763334/chingyhasasmallcock.gif')
    embed.set_footer(text='FRK Tarkov Carries', icon_url='https://media.discordapp.net/attachments/798922297062850600/800336476826763334/chingyhasasmallcock.gif')
    embedMessage = await ctx.send(embed=embed)
    await embedMessage.add_reaction('📩')


@client.event
async def on_raw_reaction_add(payload):
    guild = client.get_guild(payload.guild_id)
    payloadChannel = guild.get_channel(payload.channel_id)
    if payload.emoji.name == "📩":
        ticketCategory = discord.utils.get(guild.categories, id=844312009972383816)
        if payload.channel_id == 844312137086140426:
            userMention = f'<@{payload.member.id}>'
            requestSupportChannel = client.get_channel(844312137086140426)
            requestSupportMessage = await requestSupportChannel.fetch_message(844312429403963412) #Put id in
            for channel in ticketCategory.channels:
                userName = payload.member.name
                try:
                    channelNameSplit = channel.name
                    ticket, name = channelNameSplit.split("-", 1)
                    if userName.lower() == name:
                        await channel.send(userMention)
                        embed = discord.Embed(description='You need to close this ticket to open another one!')
                        await channel.send(embed=embed)
                        await requestSupportMessage.remove_reaction(emoji=payload.emoji,member=payload.member)
                        return
                    else:
                        pass
                except ValueError:
                    pass
            verified = discord.utils.get(guild.roles, name=f"Verified")
            carrier = discord.utils.get(guild.roles, name=f"🔐 Carrier")
            everyone = discord.utils.get(guild.roles, name=f"@everyone")
            staff = discord.utils.get(guild.roles, name="🔐 Carrier")
            embed = discord.Embed(title='FRK Carries', description=f"A {staff.mention} member will be with you shortly")
            embed.add_field(name="\nClosing the ticket", value="To close the ticket react with 🔒 and then ✅", inline=False)
            embed.set_footer(text='FRK Tarkov Carries', icon_url="https://media.discordapp.net/attachments/798922297062850600/800336476826763334/chingyhasasmallcock.gif")
            ticketChannel = await guild.create_text_channel(name=f'ticket-{payload.member.name}', category=ticketCategory)
            ticketEmbed = await ticketChannel.send(embed=embed)
            await ticketEmbed.add_reaction("🔒")
            await ticketChannel.set_permissions(verified, view_channel=False)
            await ticketChannel.set_permissions(everyone, view_channel=False)
            await ticketChannel.set_permissions(carrier, view_channel=True)
            await ticketChannel.set_permissions(payload.member, view_channel=True)
            await requestSupportMessage.remove_reaction(emoji=payload.emoji,member=payload.member)
    if payloadChannel.name.startswith("ticket"):
        if payload.emoji.name == "🔒":
            if payload.member.id == 810906858041770004:
                return
            else:
                embed = discord.Embed()
                embed = discord.Embed(description='React with ✅ below to close ticket')
                confirmMessage = await payloadChannel.send(embed=embed)
                await confirmMessage.add_reaction("✅")
        elif payload.emoji.name == "✅":
            if payload.member.id == 810906858041770004:
                return
            else:
                embed = discord.Embed(description='Ticket will close in 5 seconds')
                await payloadChannel.send(embed=embed)
            #    limit = None
            #    conversationUsers = []
            #    async for message in payloadChannel.history(limit=None):
            #        if message.author.id in conversationUsers or message.author.id == 810906858041770004:
            #            pass
            #        else:
            #            conversationUsers.append(message.author.id)
            #    transcript = await chat_exporter.export(payloadChannel, limit)
            #    transcript_file = discord.File(io.BytesIO(transcript.encode()),filename=f"transcript-{payloadChannel.name}.html")
            #    transcriptChannel = client.get_channel(835214538004889600)
            #    embed = discord.Embed(title=f'{payloadChannel.name} closed', description=f"Ticket was closed by {payload.member}", timestamp=datetime.datetime.now())
            #    embed.set_footer(text=f"EURT",icon_url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
            #   for memberid in conversationUsers:
            #        dmUser = guild.get_member(memberid)
            #        dmChannel = await dmUser.create_dm()
            #        await dmChannel.send(embed=embed, file=transcript_file)
            #   await transcriptChannel.send(embed=embed)
            await asyncio.sleep(5)
            await payloadChannel.delete()

  



client.run('ODEwOTA2ODU4MDQxNzcwMDA0.YCqd3A.9_027yZ0EJ7QDm4R1YakCzTkMQ0')