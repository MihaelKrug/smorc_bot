# bot.py
import discord
import asyncio
import logging
import os

# logging config and decorator setup

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO, filename='bot.log', filemode='w')

def log_start(func):
	def wrapper(message, *args, **kwargs):
		logging.info('%s:START:%s', func.__name__, message.content)
		return func(message, *args, **kwargs)
	return wrapper

# command handler
class CommandHandler:

	def __init__(self, client):
		self.client = client
		self.commands = []

	def add_command(self, command):
		self.commands.append(command)

	async def command_handler(self, message):
		for command in self.commands:
			for trigger in command['triggers']:
				if message.content.startswith(trigger):					
					args = message.content.split(' ')
					args.pop()
					if 'source' in command:
						logging.INFO('%s', command['source'])
						return await command['function'](message, self.client, command['source'])
					elif len(args) < command['args_num']:
						# if command needs args and they are NOT present
						await self.client.send_message(message.channel, 'command "{}" requires {} argument(s) "{}"'.format(trigger, command['args_num'], ', '.join(command['args_name'])))
					else:
						await command['function'](message, self.client, args)
					break

# create discord client
client = discord.Client()
token = os.environ["TOKEN"]

# create the CommandHandler object and pass it the client
ch = CommandHandler(client)

# command's functions
@log_start
async def hello_function(message, client, args):
	try:
		await client.send_message(message.channel, f'Hello, {message.author} !')
	except Exception as e:
		logging.exception('Exception occured')

@log_start
async def play_all_stars(message, client, args=None):
	server = message.server
	for channel in server.channels:
		if (channel.type == discord.ChannelType.voice) and (message.author in channel.voice_members):
			voice_client = await client.join_voice_channel(channel)
			player = await voice_client.create_ytdl_player('https://www.youtube.com/watch?v=L_jWHffIx5E')
			await player.start()
			break

@log_start
async def post_smorc(message, client, *args):
	try:
		e = discord.Embed(type='rich')
		e.set_image(url="https://qph.fs.quoracdn.net/main-qimg-a0cd3de7def391be918bb01604972670-c")
		await client.send_message(message.channel, embed=e)
	except Exception as e:
		logging.exception('Exception occured')

# commands to handle messages

# mosh pit https://www.youtube.com/watch?v=6BeWRJzMVU8&t=6

ch.add_command({
	'triggers': ['!hello'],
	'function': hello_function,
	'args_num': 0,
	'args_name': [],
	'description': 'Will respond hello to the caller'
})

ch.add_command({
	'triggers': ['!allstars'],
	'function': play_all_stars,
	'args_num': 0,
	'args_name': [],
	'description': 'Will play Smash Mouth - All Stars'
})

ch.add_command({
	'triggers': ['SMOrc', 'сморк', 'smorc'],
	'function': post_smorc,
	'args_num': 0,
	'args_name': [],
	'description': 'Posts SMOrc image'
})

# on booting up
@client.event
async def on_ready():
	try:
		print(client.user.name)
		print(client.user.id)
	except Exception as e:
		print(e)

# on new message
@log_start
@client.event
async def on_message(message):
	if message.author == client.user:
		pass
	else:		
		try:
			await ch.command_handler(message)			
		except TypeError as e:
			# message doesn't contain a command trigger
			pass		
		except Exception as e:
			print(e)

# run bot (run asyncio loop)
client.run(token)
