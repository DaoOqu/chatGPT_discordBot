import os
import discord
from discord.ext import commands
from revChatGPT.ChatGPT import Chatbot
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

BOT_NAME = "ChatGPT_Bot"

chatbot = Chatbot({
  "session_token": "<session_token>"
}, conversation_id=None, parent_id=None)

chatbot.ask(f"""
A conversation between multiple friends on a discord group chat. 
{BOT_NAME} responses DO NOT contain a questions. 
Only generate one {BOT_NAME} response.
{BOT_NAME} doesn't speak in perfect english.
If a user isn't speaking to {BOT_NAME}, {BOT_NAME} reponds with N/A

DO NOT INCLUDE QUESTIONS

users_name1: user_name2 what you up to?
{BOT_NAME}: N/A

users_name2: nothing much
{BOT_NAME}: N/A

users_name1: And what about you {BOT_NAME}, whats up!
{BOT_NAME}: im just chilling atm

users_name1: Cool, would you mind if we had a chat for a bit""", conversation_id=None, parent_id=None)

bot = commands.Bot(command_prefix="$")


# Starting Bot
@bot.event
async def on_ready():
  print(f"logged in as {bot.user}")

  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="study tunes"))

# Replying to a message
@bot.event
async def on_message(message):
  username = str(message.author).split('#')[0]
  user_message = str(message.content)

  if message.author == bot.user:
    return

  response = chatbot.ask(f"{username}: {user_message}", conversation_id=None, parent_id=None)
  print(response)

  if f"{BOT_NAME}: " in response["message"] and f"{BOT_NAME}: N/A" not in response["message"]:
      await message.channel.send(response["message"].replace(f"{BOT_NAME}: ", ""))
  else:
    print("Error")

bot.run(DISCORD_TOKEN)