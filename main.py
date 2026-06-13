import discord
from discord.ext import commands
from model import get_class
import os, random
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("BASE_DIR:", BASE_DIR)
print("Modelo:", os.path.join(BASE_DIR, "keras_model.h5"))
print("Existe modelo?", os.path.exists(os.path.join(BASE_DIR, "keras_model.h5")))
print("Labels:", os.path.join(BASE_DIR, "labels.txt"))
print("Existe labels?", os.path.exists(os.path.join(BASE_DIR, "labels.txt")))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''The duck command returns the photo of the duck'''
    print('hello')
    image_url = get_duck_image_url()
    await ctx.send(image_url)


@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{attachment.filename}")
            await ctx.send(
                get_class(
                    model_path=os.path.join(BASE_DIR, "keras_model.h5"),
                    labels_path=os.path.join(BASE_DIR, "labels.txt"),
                    image_path=f"./{attachment.filename}"
                )
            )
    else:
        await ctx.send("Você esqueceu de enviar a imagem :(")


bot.run('token')
