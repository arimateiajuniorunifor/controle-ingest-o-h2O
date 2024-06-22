from telegram import Bot
from dotenv import load_dotenv
import os


# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o token do bot da variável de ambiente
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def get_updates(token):
    
    bot = Bot(token=token)
    updates = bot.get_updates()
    for update in updates:
        print(update)

if __name__ == "__main__":
    get_updates(TOKEN)
