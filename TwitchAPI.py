from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from obsws import *
from dotenv import load_dotenv

import os
import asyncio
import random

load_dotenv() 

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
TARGET_CHANNEL = os.getenv('TARGET_CHANNEL')

USER_SCOPE = [
    AuthScope.CHAT_READ,
    AuthScope.CHAT_EDIT,
    #AuthScope.USER_READ_FOLLOWERS,
    AuthScope.CHANNEL_READ_SUBSCRIPTIONS,
    AuthScope.CHANNEL_READ_REDEMPTIONS,
    AuthScope.CHANNEL_MANAGE_BROADCAST,
    #AuthScope.CHANNEL_MANAGE_POLL,
    #AuthScope.CHANNEL_MODERATE_READ,
    #AuthScope.USER_MANAGE_FOLLOWERS,
    #AuthScope.USER_MANAGE_SUBSCRIPTIONS,
    AuthScope.USER_MANAGE_BLOCKED_USERS
]

# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    # join our target channel, if you want to join multiple, either call join for each individually.
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here


# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')
    if msg.text == "Follow":
        alert(18, 21, msg.user.name, "Follower")
    if msg.text == "Sub":
        alert(18, 21, msg.user.name, "Subscriber")


# this will be called whenever someone subscribes to a channel
async def on_sub(sub: ChatSub):
    print(f'New subscription in {sub.room.name}:\\n'
          f'  Type: {sub.sub_plan}\\n'
          f'  Message: {sub.sub_message}')

# this will be called whenever the !reply command is issued
async def test_command(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        await cmd.reply('you did not tell me what to reply with')
    else:
        await cmd.reply(f'{cmd.user.name}: {cmd.parameter}')

async def list_commands(cmd: ChatCommand):
    await cmd.reply(f"Available commands: \n!reply <message> \n!beancounter <username> \n!commands")

async def paper_scissors_rock(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        await cmd.reply('You must choose either rock, paper, or scissors')
    elif cmd.parameter != 'rock' or cmd.parameter != 'paper' or cmd.parameter != 'scissors':
        await cmd.reply('You must choose either rock, paper, or scissors')
    else:
        robotChoice = random.choice(['rock', 'paper', 'scissors'])

        if cmd.parameter == robotChoice:
            await cmd.reply(f"{cmd.user.name} chose {cmd.parameter}, I chose {robotChoice}. It's a tie!")
        elif cmd.parameter == 'rock' and robotChoice == 'paper':
            await cmd.reply(f"{cmd.user.name} chose {cmd.parameter}, I chose {robotChoice}. I win!")
        elif cmd.parameter == 'rock' and robotChoice == 'scissors':
            await cmd.reply(f"{cmd.user.name} chose {cmd.parameter}, I chose {robotChoice}. You win!")
        elif cmd.parameter == 'paper' and robotChoice == 'rock':
            await cmd.reply(f"{cmd.user.name} chose {cmd.parameter}, I chose {robotChoice}. You win!")
        elif cmd.parameter == 'paper' and robotChoice == 'scissors':
            await cmd.reply(f"{cmd.user.name} chose {cmd.parameter}, I chose {robotChoice}. I win!")
        elif cmd.parameter == 'scissors' and robotChoice == 'rock':
            await cmd.reply(f"{cmd.user.name} chose {cmd.parameter}, I chose {robotChoice}. I win!")
        elif cmd.parameter == 'scissors' and robotChoice == 'paper':
            await cmd.reply(f"{cmd.user.name} chose {cmd.parameter}, I chose {robotChoice}. You win!")


        
# Example function to handle events
async def handle_follow_event(event_data):
    print(f"Received follow event: {event_data}")

# this is where we set up the bot
async def run():
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    chat = await Chat(twitch)
    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    # listen to channel subscriptions
    chat.register_event(ChatEvent.SUB, on_sub)
    # there are more events, you can view them all in this documentation

    # you can directly register commands and their handlers, this will register the !reply command
    chat.register_command('reply', test_command)
    chat.register_command('commands', list_commands)
    chat.register_command('psr', paper_scissors_rock)

    # we are done with our setup, lets start this bot up!
    chat.start()

# lets run our setup
asyncio.run(run())
