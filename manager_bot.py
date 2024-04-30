from dotenv import load_dotenv
import os
import discord
#import openai
import pandas as pd
import asyncio
from discord.ext import commands
from discord.ext import commands
from discord.ui import Button, View

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = 1223507114266198210
reminders = {}

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
@bot.event
async def on_ready():
    print("Hello, I'm alive!")
    channel = bot.get_channel(CHANNEL_ID)
    bot.add_view(Verify())
    await channel.send("Hi! I'm alive")


@bot.command(help="Says hello to the user.")
async def hello(ctx):
    await ctx.send("Hi!" + ctx.author.mention) 

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

@bot.command(help="Open verify box to verify. Usage: !verify")
async def verify(ctx):
    embed = discord.Embed(title = "Role Selection Form", description = "Press to add/remove a role.")
    await ctx.send(embed = embed, view = Verify())

@bot.command(help="Checks your BC email. Usage: !check_email [your emain address]")
async def check_email(ctx, user_email: str):
    try:      
        df = pd.read_excel('Your path to the excel file')

        if user_email in df['Emails'].values:
            await ctx.send("The email is in the Excel file.")
        else:
            await ctx.send("The email is not in the Excel file.")
    except FileNotFoundError:
        await ctx.send("The Excel file was not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(help="Creates a new ticket. Usage: !create_ticket [reason]")
async def create_ticket(ctx):
    guild = ctx.guild
    ticket_category = discord.utils.get(guild.categories, name='Tickets')

    if not ticket_category:
        ticket_category = await guild.create_category('Tickets')

    ticket_channel = await guild.create_text_channel(f'ticket-{ctx.author.display_name}', category=ticket_category)

    await ticket_channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ticket_channel.set_permissions(ctx.author, view_channel=True)

    await ticket_channel.send(f'Hi {ctx.author.mention}, welcome to your ticket! Please describe your issue.')
    await ctx.send(f'{ctx.author.mention}, your ticket has been created: {ticket_channel.mention}.')

@bot.command(help="Close your ticket. Usage: !close_ticket")
async def close_ticket(ctx):
    if ctx.channel.category and ctx.channel.category.name == 'Tickets':
        await ctx.send('Closing this ticket in 5 seconds...')
        await asyncio.sleep(5)
        await ctx.channel.delete()
    else:
        await ctx.send('You can only use this command in a ticket channel.')

@bot.command(help="Creates a new Poll with limit of 10 vote options. Usage: !poll [option 1] [option 2] [option ...] [option 10] [Title of the poll]")
async def poll(ctx, *options: str, title):
    if len(options) < 2:
        await ctx.send("Error: A poll must have at least two options.")
        return
    if len(options) > 10:
        await ctx.send("Error: A poll cannot have more than 10 options.")
        return

    emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    description = []
    for x, option in enumerate(options):
        description.append(f"{emojis[x]} {option}")
    embed = discord.Embed(title=title, description='\n'.join(description))
    embed.set_footer(text="React to vote!")

    poll_message = await ctx.send(embed=embed)
    for emoji in emojis[:len(options)]:
        await poll_message.add_reaction(emoji)

@bot.command(help="End your poll. Usage: !endpoll [message id of the poll]")
async def endpoll(ctx, message_id: int):
    try:
        message = await ctx.channel.fetch_message(message_id)
    except discord.NotFound:
        await ctx.send("Poll message not found.")
        return
    except discord.HTTPException:
        await ctx.send("Failed to retrieve the message.")
        return

    if not message.embeds:
        await ctx.send("Provided message ID does not contain a poll.")
        return

    embed = message.embeds[0]
    if not embed.footer.text.startswith("React to vote!"):
        await ctx.send("Provided message does not seem to be a poll created by me.")
        return

    results = []
    for reaction in message.reactions:
        if reaction.is_custom_emoji():  
            continue

        users = [user async for user in reaction.users() if not user.bot]
        vote_count = len(users)
        results.append((reaction.emoji, vote_count))

    if not results:
        await ctx.send("No votes were cast.")
        return

    results.sort(key=lambda x: x[1], reverse=True)
    results_description = "\n".join([f"{emoji}: {count} votes" for emoji, count in results])

    results_embed = discord.Embed(title="Poll Results", description=results_description)
    await ctx.send(embed=results_embed)


@bot.command(help="Create a reminder for you. Usage: !remind [time] [minutes/hours] [message] ")
async def remind(ctx, interval: float, unit: str, *, message: str):
    if unit not in ["minutes", "hours"]:
        await ctx.send("Error: The unit must be 'minutes' or 'hours'.")
        return

    if unit == "hours":
        interval *= 60

    interval_seconds = interval * 60

    await ctx.send(f"Reminder set! I will remind you every {interval} {unit} with the message: \"{message}\"")

    task = asyncio.create_task(send_reminders(ctx, interval_seconds, message))
    reminders[(ctx.author.id, message)] = task

async def send_reminders(ctx, interval_seconds, message):
    try:
        while True:
            await asyncio.sleep(interval_seconds)
            await ctx.send(f'{ctx.author.mention}, {message}')
    except asyncio.CancelledError:
        await ctx.send(f'Reminder canceled: {message}')

@bot.command(help="Stop the reminder. Usage: !stopremind [message] ")
async def stopremind(ctx, *, message: str):
    reminder_key = (ctx.author.id, message)

    if reminder_key in reminders:
        reminders[reminder_key].cancel() 
        del reminders[reminder_key]
        await ctx.send(f"Your reminder for \"{message}\" has been stopped.")
    else:
        await ctx.send("No active reminder found with that message.")


bot.run(BOT_TOKEN)