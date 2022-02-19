import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

load_dotenv('.env')
bot = commands.Bot(command_prefix="!")


async def timer():
    await bot.wait_until_ready()
    channel = bot.get_channel(943142720568954931)
    msg_sent = False
    

    while True:
        base_url = "https://www.freecodecamp.org"
        req = requests.get("https://www.freecodecamp.org/news/tag/python/")
        soup = BeautifulSoup(req.text, 'lxml')

        posts_section = soup.find('section', class_="post-feed")
        posts = posts_section.find_all('article', class_="post-card")

        for post in posts:
            half_link = post.a['href']
            link = base_url + half_link

            img_link = post.find('img', class_="post-card-image").attrs['src']
            
            heading = post.find('h2', class_="post-card-title").text.strip()

            with open('post_name.txt', 'r') as f:
                if heading not in f.read():
                    embed = discord.Embed(title=heading, url=link)
                    embed.set_image(url=img_link)
                    with open('post_name.txt', 'a') as f:
                        f.write(heading + '\n')
                        await channel.send(embed=embed)

                else:
                    msg_sent=False

        await asyncio.sleep(14400)


bot.loop.create_task(timer())
bot.run(os.getenv('TOKEN'))