from dotenv import load_dotenv
import os
import discord
import pandas as pd
from discord.ext import commands
from discord.ext import commands
from discord.ui import Button, View

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = 1223507114266198210

bad_words = [ "dumb", "stupid"]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
@bot.event
async def on_ready():
    print("Hello, I'm alive!")
    channel = bot.get_channel(CHANNEL_ID)
    bot.add_view(Verify())
    await channel.send("Hi! I'm alive")

@bot.command()
async def xinchao(ctx):
    await ctx.send("Chao ban!" + ctx.author.mention) 

class Verify(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label="Verify", custom_id="Verify", style=discord.ButtonStyle.success)

    async def button1(self, interaction, button):
        role = 1224909783258234980
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message("You have removed a role!", ephemeral = True)
        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message("You have added a role!", ephemeral = True)

@bot.command()
async def verify(ctx):
    embed = discord.Embed(title = "Role Selection Form", description = "Press to add/remove a role.")
    await ctx.send(embed = embed, view = Verify())

@bot.command()
async def check_email(ctx, user_email: str):
    try:
        
        df = pd.read_excel('C:\\Users\\tungv\\Downloads\\example_emails.xlsx')

        if user_email in df['Emails'].values:
            await ctx.send("The email is in the Excel file.")
        else:
            await ctx.send("The email is not in the Excel file.")
    except FileNotFoundError:
        await ctx.send("The Excel file was not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    for bad_word in bad_words:
        if bad_word.lower() in message.content.lower():
            await message.delete()
            warning = f"{message.author.mention}, please do not use bad language!"
            await message.channel.send(warning)
            return
    

    await bot.process_commands(message)


bot.run(BOT_TOKEN)