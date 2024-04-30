import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)  # No timeout for the view

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, custom_id="open_ticket")
    async def ticket_button(self, button: Button, interaction: discord.Interaction):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        }
        ticket_channel = await guild.create_text_channel(f"ticket-{interaction.user}", overwrites=overwrites)
        await ticket_channel.send(f"Hi {interaction.user.mention}, how can we help you?")
        await interaction.response.send_message(f"Ticket channel created: {ticket_channel.mention}", ephemeral=True)

@bot.command()
async def mytickets(ctx):
    ticket_view = TicketView()  # Initialize the view here
    # Check for all channels that start with 'ticket-' and where the user has access
    ticket_channels = [channel for channel in ctx.guild.text_channels if channel.name.startswith("ticket-") and ctx.author in channel.members]
    if ticket_channels:
        tickets = "\n".join(channel.mention for channel in ticket_channels)
        await ctx.send(f"Here are your ticket channels:\n{tickets}", view=ticket_view)
    else:
        await ctx.send("You do not have any open tickets.", view=ticket_view)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

bot.run('MTIyMzUwNDY2MjUzMTkzMjE5MA.GcsK0J.6wkpSY0xz5vZLhH2ZZ3rM6MRt2d8LwvVKo72VE')
