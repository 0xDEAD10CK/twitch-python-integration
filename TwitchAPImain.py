from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from obsws import *
from dotenv import load_dotenv
import threading

import os
import subprocess
import asyncio
import random
from typing import Awaitable

load_dotenv() 

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
TARGET_CHANNEL = os.getenv('TARGET_CHANNEL')

# Initialize empty names for both subscriber and follower
recent_subscriber = ""
recent_follower = ""

with open('recentFollow.txt', 'r') as f:
    recent_follower = f.read()
    f.close()

with open('recentSub.txt', 'r') as f:
    recent_subscriber = f.read()
    f.close()

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
    threading.Thread(target=spin_chat).start()
    # join our target channel, if you want to join multiple, either call join for each individually.
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here

# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')
    with open('chat.txt', 'a') as f:
        f.write(f'{msg.user.name}: {msg.text}\n\n')
        f.close()

async def update_recent_activity(subscriber_name: str, follower_name: str):
    with open('recentActivity.txt', 'w') as f:
        f.write(f" || Most Recent Sub: {subscriber_name} || Most Recent Follow: {follower_name}")

# this will be called whenever someone subscribes to a channel
async def on_sub(event: dict) -> Awaitable[None]:
    global recent_subscriber
    recent_subscriber = event.event.user_name

    with open('recentSub.txt', 'w') as f:
        f.write(recent_subscriber)
        f.close()

    alert(18, 21, 24, event.event.user_name, "Subscriber")

    await update_recent_activity(recent_subscriber, recent_follower)

async def on_follow(event: dict) -> Awaitable[None]:
    global recent_follower
    recent_follower = event.event.user_name

    with open('recentFollower.txt', 'w') as f:
        f.write(recent_follower)
        f.close()

    alert(18, 21, 24, event.event.user_name, "Follower")

    await update_recent_activity(recent_subscriber, recent_follower)


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
        TARGET_CHANNEL_ID = user.id
        break  # Extract the first user and exit the loop

    # create chat instance
    chat = await Chat(twitch)

    # create eventsub instance
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()

    # register the eventsub subscriptions
    await eventsub.listen_channel_follow_v2(broadcaster_user_id=str(TARGET_CHANNEL_ID), moderator_user_id=str(TARGET_CHANNEL_ID), callback=on_follow)
    await eventsub.listen_channel_subscribe(broadcaster_user_id=str(TARGET_CHANNEL_ID), callback=on_sub)
    #await eventsub.listen_channel_points_custom_reward_redemption_update

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
