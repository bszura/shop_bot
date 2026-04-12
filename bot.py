import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user} jest online!')
    print(f'✅ Zalogowano jako: {bot.user.name} ({bot.user.id})')
    print('━' * 50)
    
    try:
        synced = await bot.tree.sync()
        print(f'✅ Zsynchronizowano {len(synced)} komend slash')
    except Exception as e:
        print(f'❌ Błąd synchronizacji: {e}')
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="🛒 /panel | Shop Bot"
        ),
        status=discord.Status.online
    )

@bot.tree.command(name="panel", description="Wyświetla panel sklepu")
async def panel(interaction: discord.Interaction):
    
    embed = discord.Embed(
        title="🛒 PANEL SKLEPU",
        description="Witaj w naszym sklepie! Wybierz kategorię poniżej:",
        color=0x2b2d31
    )
    
    embed.add_field(
        name="💳 Produkty",
        value="Kliknij przycisk aby zobaczyć dostępne produkty",
        inline=False
    )
    
    embed.add_field(
        name="📦 Twoje zamówienia",
        value="Sprawdź status swoich zamówień",
        inline=False
    )
    
    embed.add_field(
        name="❓ Pomoc",
        value="Potrzebujesz pomocy? Skontaktuj się z supportem",
        inline=False
    )
    
    embed.set_footer(
        text="Shop Bot • Powered by Python",
        icon_url=bot.user.avatar.url if bot.user.avatar else None
    )
    
    if interaction.guild and interaction.guild.icon:
        embed.set_thumbnail(url=interaction.guild.icon.url)
    
    class ShopButtons(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        
        @discord.ui.button(label="🛍️ Produkty", style=discord.ButtonStyle.green, custom_id="products")
        async def products_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            products_embed = discord.Embed(
                title="🛍️ DOSTĘPNE PRODUKTY",
                description="Oto nasza oferta:",
                color=0x00ff00
            )
            products_embed.add_field(name="📦 Produkt #1", value="Cena: 50 zł\nOpis: Przykładowy produkt", inline=False)
            products_embed.add_field(name="📦 Produkt #2", value="Cena: 100 zł\nOpis: Premium produkt", inline=False)
            await interaction.response.send_message(embed=products_embed, ephemeral=True)
        
        @discord.ui.button(label="📦 Moje zamówienia", style=discord.ButtonStyle.blurple, custom_id="orders")
        async def orders_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            orders_embed = discord.Embed(
                title="📦 TWOJE ZAMÓWIENIA",
                description="Brak aktywnych zamówień",
                color=0x3498db
            )
            await interaction.response.send_message(embed=orders_embed, ephemeral=True)
        
        @discord.ui.button(label="💰 Portfel", style=discord.ButtonStyle.gray, custom_id="wallet")
        async def wallet_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            wallet_embed = discord.Embed(
                title="💰 TWÓJ PORTFEL",
                description=f"Saldo: **0 zł**\n\nID użytkownika: `{interaction.user.id}`",
                color=0x95a5a6
            )
            await interaction.response.send_message(embed=wallet_embed, ephemeral=True)
        
        @discord.ui.button(label="❓ Pomoc", style=discord.ButtonStyle.red, custom_id="help")
        async def help_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            help_embed = discord.Embed(
                title="❓ POMOC",
                description="Potrzebujesz pomocy?\n\nSkontaktuj się z administracją serwera!",
                color=0xe74c3c
            )
            await interaction.response.send_message(embed=help_embed, ephemeral=True)
    
    await interaction.response.send_message(embed=embed, view=ShopButtons())

@bot.tree.command(name="info", description="Informacje o bocie")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="ℹ️ Informacje o bocie",
        color=0x3498db
    )
    embed.add_field(name="🏓 Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="👥 Serwery", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="👤 Użytkownicy", value=str(len(bot.users)), inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f'Error: {error}')

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)