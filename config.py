import os
from dotenv import load_dotenv

load_dotenv() # Carrega variáveis de ambiente do arquivo .env

# --- CONFIGURAÇÕES GERAIS DO BOT ---
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = "/"
GUILD_ID = 1414809066601054311  # ID do seu servidor

# --- CONFIGURAÇÕES DO SISTEMA DE TICKET ---
TICKET_CATEGORY_ID = 1430234319942844581  # ID da categoria onde os canais de ticket serão criados
STAFF_ROLE_ID = 1430228364551262450      # ID do cargo de administradores/staff
BOOSTER_ROLE_ID = 1430308508041220157     # ID do cargo de Booster 
PANEL_CHANNEL_ID = 1430307570488447107  # Canal onde será enviado o painel