import discord
from discord.ext import commands
import os

# Importa as configurações do arquivo config.py
import config

# ===== CLASSE PRINCIPAL DO BOT =====
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True  # Habilita a intent de conteúdo de mensagem
        super().__init__(command_prefix=config.COMMAND_PREFIX, intents=intents)

    async def setup_hook(self):
        """Este método é chamado uma vez quando o bot é iniciado."""
        # Constrói um caminho absoluto para a pasta cogs para evitar erros de diretório
        cogs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cogs')

        # Carrega todos os arquivos .py na pasta 'cogs' como extensões
        for filename in os.listdir(cogs_path):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"✅ Cog '{filename[:-3]}' carregado com sucesso.")
                except Exception as e:
                    print(f"❌ Falha ao carregar o cog '{filename[:-3]}'. Erro: {e}")

        # Sincroniza os comandos de aplicação (slash commands) com o servidor especificado
        await self.tree.sync(guild=discord.Object(id=config.GUILD_ID))

    async def on_ready(self):
        print(f"🚀 Bot conectado como {self.user} e comandos sincronizados!")

if __name__ == "__main__":
    if not config.BOT_TOKEN:
        print("❌ ERRO: O token do bot não foi encontrado. Verifique seu arquivo .env e a variável DISCORD_TOKEN.")
    else:
        # Instancia e executa o bot apenas se o token for encontrado
        print("▶️  Inicializando o bot...")
        bot = MyBot()
        bot.run(config.BOT_TOKEN)
