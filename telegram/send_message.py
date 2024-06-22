import os
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o token e o ID do chat das variáveis de ambiente
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_message(token, chat_id, message):
    try:
        bot = Bot(token=token)
        bot.send_message(chat_id=chat_id, text=message)
        print("Mensagem enviada com sucesso!")
    except TelegramError as e:
        print(f"Erro ao enviar mensagem: {e}")

if __name__ == "__main__":
    MESSAGE = 'Olá, esta é uma mensagem de teste!'
    send_message(TOKEN, CHAT_ID, MESSAGE)
