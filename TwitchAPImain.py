from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from obsws import *
from dotenv import load_dotenv

import os
import subprocess
import asyncio
import random
from typing import Awaitable

load_dotenv() 

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
TARGET_CHANNEL = os.getenv('TARGET_CHANNEL')

USER_SCOPE = [
    AuthScope.CHAT_READ,
    AuthScope.CHAT_EDIT,
    AuthScope.CHANNEL_READ_SUBSCRIPTIONS,
    AuthScope.CHANNEL_READ_REDEMPTIONS,
    AuthScope.CHANNEL_MANAGE_BROADCAST,
    AuthScope.USER_MANAGE_BLOCKED_USERS,
    AuthScope.MODERATOR_READ_FOLLOWERS
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
        alert(18, 21, 24, msg.user.name, "Follower")
    if msg.text == "Sub":
        alert(18, 21, 24, msg.user.name, "Subscriber")

# this will be called whenever someone subscribes to a channel
async def on_sub(sub: ChatSub):
    print(f'New subscription in {sub.room.name}:\\n'
          f'  Type: {sub.sub_plan}\\n'
          f'  Message: {sub.sub_message}')

async def on_follow(event: dict) -> Awaitable[None]:
    alert(18, 21, 24, event.event.user_name, "Follower")

# this will be called whenever the !reply command is issued
async def test_command(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        await cmd.reply('you did not tell me what to reply with')
    else:
        await cmd.reply(f'{cmd.user.name}: {cmd.parameter}')

async def list_commands(cmd: ChatCommand):
    await cmd.reply(f"Available commands: \n!reply <message> \n!beancounter <username> \n!commands")


# this is where we set up the bot
async def run():
    global TARGET_CHANNEL
    user = None
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # Fetch the user ID for the channel using async generator
    async for user in twitch.get_users(logins=[TARGET_CHANNEL]):
        print('1. ', user)
        TARGET_CHANNEL_ID = user.id
        print('2.', TARGET_CHANNEL_ID)
        break  # Extract the first user and exit the loop

    # create chat instance
    chat = await Chat(twitch)

    # create eventsub instance
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()

    print('3. ', user)
    print('4. ', TARGET_CHANNEL_ID)

    print(eventsub.connection_url)

    # register the eventsub subscription
    await eventsub.listen_channel_follow_v2(
        broadcaster_user_id=str(TARGET_CHANNEL_ID),
        moderator_user_id=str(TARGET_CHANNEL_ID),
        callback=on_follow
    )

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

    # we are done with our setup, lets start this bot up!
    chat.start()


# lets run our setup
asyncio.run(run())
