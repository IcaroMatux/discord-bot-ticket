import discord
from discord import app_commands
from discord.ext import commands
import logging

import asyncio

# Importa as configurações diretamente. Como o bot é iniciado a partir de main.py,
# a pasta raiz já está no caminho de busca do Python.
import config

# Configura um logger específico para este arquivo
logger = logging.getLogger(__name__)



# ===== DROPDOWN (Select Menu) =====
class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="EloBoost", description="Abrir ticket de EloBoost", emoji="🎮"),
            discord.SelectOption(label="DuoBoost", description="Abrir ticket de DuoBoost", emoji="👥"),
            discord.SelectOption(label="Coach", description="Abrir ticket de Coach", emoji = "💪"),
        ]
        super().__init__(
            placeholder="Selecione o tipo de ticket...",
            options=options,
            min_values=1,
            max_values=1,
            custom_id="ticket_select_menu" # ID único para o menu persistente
        )

    async def callback(self, interaction: discord.Interaction):
        categoria = self.values[0]

        embed = discord.Embed(
            title=f"Categoria selecionada: {categoria}",
            description="Clique no botão abaixo para abrir seu ticket.",
            color=discord.Color.blue()
        )
        embed.set_image(url="https://exemplo.com/imagem_principal.jpg")
        embed.set_thumbnail(url="https://exemplo.com/thumb.jpg")

        # A classe TicketButtonView já cria a view e adiciona o botão.
        view = TicketButtonView(categoria=categoria)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


# ===== BOTÃO DE ABRIR TICKET =====
class TicketButton(discord.ui.Button):
    def __init__(self, categoria: str):
        super().__init__(label="Abrir Ticket", style=discord.ButtonStyle.green)
        self.categoria = categoria

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = guild.get_channel(config.TICKET_CATEGORY_ID)
        staff_role = guild.get_role(config.STAFF_ROLE_ID)
        booster_role = guild.get_role(config.BOOSTER_ROLE_ID)

        # Validação para garantir que a categoria e o cargo foram encontrados
        if not category or not staff_role or not booster_role:
            await interaction.response.send_message(
                "❌ Erro de configuração do bot. Contate um administrador.",
                ephemeral=True
            )

            logger.error(f"Erro de configuração ao criar ticket: Categoria={category} Staff={staff_role} Booster={booster_role}")
            return

        channel_name = f"ticket-{interaction.user.name}-{self.categoria}".replace(" ", "-").lower()

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            staff_role: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            booster_role: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        }

        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            reason=f"Ticket criado por {interaction.user} para {self.categoria}"
        )

        # Cria a view com o botão de fechar
        close_view = CloseTicketView()
        await channel.send(
          f"Bem vindo, {interaction.user.mention}! Você abriu um ticket de **{self.categoria}**.\n"
          f"A equipe ({staff_role.mention} e {booster_role.mention}) já foi notificada e responderá em breve.",
          view=close_view
        )
        await interaction.response.send_message(f"✅ Seu ticket foi criado com sucesso!: {channel.mention}", ephemeral=True)


# ===== BOTÃO DE FECHAR TICKET =====

class CloseTicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Fechar Ticket",
            style=discord.ButtonStyle.red,
            emoji="🔒",
            custom_id="close_ticket_button" # custom_id é necessário para views persistentes
        )

    async def callback(self, interaction: discord.Interaction):
        user_roles_ids = [role.id for role in interaction.user.roles]
        if config.STAFF_ROLE_ID not in user_roles_ids and config.BOOSTER_ROLE_ID not in user_roles_ids:
            await interaction.response.send_message("❌ Você não tem permissão para fechar este ticket.", ephemeral=True)
            return

        # Envia uma mensagem de confirmação antes de deletar 
        await interaction.response.send_message(f"🔒 Ticket marcado para fechar por {interaction.user.mention}. Este canal será excluído em 5 segundos.")

        # Espera 5 segundos para fechar o ticket
        await asyncio.sleep(5)
        await interaction.channel.delete(reason=f"Ticket fechado por {interaction.user.name}")


# View que contém o botão de fechar
class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CloseTicketButton())


class TicketButtonView(discord.ui.View):
    def __init__(self, categoria: str):
        # Esta view é temporária e efêmera, não precisa de timeout=None
        super().__init__(timeout=180) # Timeout de 3 minutos
        self.add_item(TicketButton(categoria))


# View que contém o menu dropdown para o painel
class TicketSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())


# ===== CLASSE DO COG =====
class TicketSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Adiciona as views persistentes para que os botões funcionem após o bot reiniciar
        self.bot.add_view(TicketSelectView())
        self.bot.add_view(CloseTicketView())

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("⚙️  Cog 'TicketSystem' pronto e views persistentes registradas.")

    @app_commands.command(name="painel", description="Envia o painel de abertura de tickets")
    @app_commands.guilds(discord.Object(id=config.GUILD_ID))
    @app_commands.checks.has_permissions(administrator=True)
    async def painel(self, interaction: discord.Interaction):
        """Envia o painel de abertura de tickets."""
        if interaction.channel.id != config.PANEL_CHANNEL_ID:
            await interaction.response.send_message(f"Use este comando no canal correto: <#{config.PANEL_CHANNEL_ID}>", ephemeral=True)
            return

        embed = discord.Embed(
            title="🎫 Sistema de Tickets",
            description="Selecione a categoria desejada no menu abaixo.",
            color=discord.Color.green()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1180606307905052752/1430656208020177037/Karthus_17.png?ex=68fa91ec&is=68f9406c&hm=02a68e42e12a4604eeb5847bb9bac9ecf4d05d6fd032b975530cbe1dae9da721&")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1180606307905052752/1430656208020177037/Karthus_17.png?ex=68fa91ec&is=68f9406c&hm=02a68e42e12a4604eeb5847bb9bac9ecf4d05d6fd032b975530cbe1dae9da721&")

        # Envia a mensagem com a view persistente que foi registrada no bot.
        await interaction.channel.send(embed=embed, view=TicketSelectView())
        await interaction.response.send_message("✅ Painel de tickets enviado com sucesso!", ephemeral=True)
        logger.info(f"Painel de tickets enviado por {interaction.user} no canal {interaction.channel.name}")


# Função `setup` que o discord.py chama para carregar o cog
async def setup(bot: commands.Bot):
    # Adiciona o Cog ao bot
    await bot.add_cog(TicketSystem(bot))