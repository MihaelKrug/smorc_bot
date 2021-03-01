import discord
import os

client = discord.Client()
token = os.environ["TOKEN"]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #if message.content.startswith('$hello'):
    #    await message.channel.send('Hello!')
    await check_message(message)


async def on_greeting(message):
	await message.channel.send('Hello!')

msg_lib = {'hello':on_greeting}

async def check_message(message):
	if message.content in list(msg_lib):
		await msg_lib[message.content](message)

client.run(token)