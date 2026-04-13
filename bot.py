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

# Select Menu Class
class ShopSelectMenu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="🛍️ Produkty",
                description="Zobacz dostępne produkty w sklepie",
                emoji="🛍️",
                value="products"
            ),
            discord.SelectOption(
                label="📦 Moje zamówienia",
                description="Sprawdź status swoich zamówień",
                emoji="📦",
                value="orders"
            ),
            discord.SelectOption(
                label="💰 Portfel",
                description="Sprawdź swoje saldo",
                emoji="💰",
                value="wallet"
            ),
            discord.SelectOption(
                label="❓ Pomoc",
                description="Skontaktuj się z supportem",
                emoji="❓",
                value="help"
            ),
        ]
        
        super().__init__(
            placeholder="🛒 Wybierz kategorię...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="shop_menu"
        )
    
    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        
        if selected == "products":
            embed = discord.Embed(
                title="🛍️ DOSTĘPNE PRODUKTY",
                description="Oto nasza oferta:",
                color=0x00ff00
            )
            embed.add_field(
                name="📦 Produkt #1",
                value="💰 Cena: **50 zł**\n📝 Opis: Przykładowy produkt premium\n🔢 Stock: 10 szt.",
                inline=False
            )
            embed.add_field(
                name="📦 Produkt #2",
                value="💰 Cena: **100 zł**\n📝 Opis: Ekskluzywny produkt VIP\n🔢 Stock: 5 szt.",
                inline=False
            )
            embed.add_field(
                name="📦 Produkt #3",
                value="💰 Cena: **25 zł**\n📝 Opis: Pakiet startowy\n🔢 Stock: Unlimited",
                inline=False
            )
            embed.set_footer(text="Aby kupić, skontaktuj się z administracją")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif selected == "orders":
            embed = discord.Embed(
                title="📦 TWOJE ZAMÓWIENIA",
                description="Historia twoich zamówień:",
                color=0x3498db
            )
            embed.add_field(
                name="Status",
                value="❌ Brak aktywnych zamówień",
                inline=False
            )
            embed.set_footer(text=f"ID użytkownika: {interaction.user.id}")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif selected == "wallet":
            embed = discord.Embed(
                title="💰 TWÓJ PORTFEL",
                description=f"**Saldo:** 0 zł\n\n💳 Dostępne metody płatności:\n• BLIK\n• Przelew bankowy\n• PayPal",
                color=0x95a5a6
            )
            embed.add_field(
                name="📊 Statystyki",
                value="🛒 Zakupy: 0\n💸 Wydano: 0 zł",
                inline=False
            )
            embed.set_footer(text=f"ID użytkownika: {interaction.user.id}")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif selected == "help":
            embed = discord.Embed(
                title="❓ POMOC & SUPPORT",
                description="Potrzebujesz pomocy?\n\n📞 **Kontakt:**\n• Otwórz ticket na serwerze\n• Napisz do administracji\n• Email: support@example.com",
                color=0xe74c3c
            )
            embed.add_field(
                name="⏰ Godziny pracy",
                value="Poniedziałek - Piątek: 9:00 - 18:00\nWeekend: 10:00 - 16:00",
                inline=False
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

# View z Select Menu
class ShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ShopSelectMenu())

# Komenda /panel
@bot.tree.command(name="panel", description="Wyświetla panel sklepu")
async def panel(interaction: discord.Interaction):
    
    embed = discord.Embed(
        title="🛒 PANEL SKLEPU",
        description="Witaj w naszym sklepie!\n\nUżyj menu poniżej, aby wybrać kategorię:",
        color=0x2b2d31
    )
    
    embed.add_field(
        name="📋 Dostępne kategorie:",
        value="🛍️ **Produkty** - Przeglądaj ofertę\n📦 **Zamówienia** - Sprawdź status\n💰 **Portfel** - Zarządzaj saldem\n❓ **Pomoc** - Skontaktuj się z nami",
        inline=False
    )
    
    embed.set_footer(
        text="Shop Bot • Powered by Python",
        icon_url=bot.user.avatar.url if bot.user.avatar else None
    )
    
    if interaction.guild and interaction.guild.icon:
        embed.set_thumbnail(url=interaction.guild.icon.url)
    
    await interaction.response.send_message(embed=embed, view=ShopView())

# Komenda /info
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
