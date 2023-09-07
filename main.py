import asyncio
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

url = "https://vk.com/bot_maxim"

headers = {
    "Accept" : "/",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text

soup = BeautifulSoup(src, "lxml")
post = None

intents = discord.Intents().all()

client = discord.Client(intents=intents)

settings = {
    'token': 'MTAyNTQzNDc3Mjc2MTIyMzM1MQ.Gmdt6f.2sx4qfQkdpZESQmJph5Lt_pxnWu0muRUGLtZSQ',
    'bot': 'Goosebot3',
    'id': 1025434772761223351,
    'prefix': '!'
}

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

@bot.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'start':
        await post_changed(message)

async def post_changed(message):
    global post
    soup = BeautifulSoup(src, "lxml")
    newpost = soup.find("div", class_="_post_content")
    if post != newpost:
        print("Пост поменялся")
        post = newpost
        await send_post(message, newpost)
    else:
        print("Пост не поменялся")
        await asyncio.sleep(30)
        await post_changed(message)

async def send_post(message, post):
    name_ofsociety = soup.find("a", class_="author")
    photourl = soup.find("img", class_="post_img")
    posttext = post.find("div", class_="wall_post_text")
    image_from = post.find_all(class_="MediaGrid__imageElement")
    link_number = soup.find("div", class_="post")
    print(link_number["data-post-id"])
    embedVar = discord.Embed(title=name_ofsociety.text, color=0x00ff00)
    if posttext:
        embedVar.description = posttext.text
    if image_from:
        embedVar.set_image(url=image_from[0]["src"])  # the image itself
    if photourl:
        embedVar.set_thumbnail(url=photourl["src"])
    await message.channel.send(embed=embedVar)
    await asyncio.sleep(30)
    await post_changed(message)

bot.run(settings['token'])
