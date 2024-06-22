from telegram import Bot

# Seu token de acesso
TOKEN = 'seu_token_aqui'

# ID do chat (pode ser o ID de um usuário ou de um grupo)
CHAT_ID = 'id_do_chat_aqui'

# A mensagem que você deseja enviar
MESSAGE = 'Olá, esta é uma mensagem de teste!'

def send_message(token, chat_id, message):
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)

# Envia a mensagem
send_message(TOKEN, CHAT_ID, MESSAGE)
