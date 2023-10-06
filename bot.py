from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler, CallbackContext
from telegram import Update

# Definindo os estados da conversa
INICIO, AGUARDANDO_MENSAGEM = range(2)

# Função para iniciar a conversa
def iniciar(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Olá! Eu sou o seu bot de atendimento. Como posso ajudá-lo hoje?"
    )
    return AGUARDANDO_MENSAGEM

# Função para lidar com mensagens recebidas
def receber_mensagem(update: Update, context: CallbackContext) -> int:
    mensagem = update.message.text
    # Lógica para processar a mensagem aqui
    update.message.reply_text(f"Você disse: {mensagem}")
    return AGUARDANDO_MENSAGEM

def main():
    # Substitua 'SEU_TOKEN_AQUI' pelo token de acesso do seu bot
    TOKEN = '6692524161:AAEnkX-5vkMGra3uvRWrk0_0cO17tlLwwK8'

    # Inicializa o Updater com o token do bot
    updater = Updater(TOKEN)

    # Obtém o despachante para registrar manipuladores
    dispatcher = updater.dispatcher

    # Define um manipulador para o estado inicial
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', iniciar)],
        states={
            AGUARDANDO_MENSAGEM: [MessageHandler(Filters.text & ~Filters.command, receber_mensagem)],
        },
        fallbacks=[],
    )

    # Registra o manipulador de conversação no despachante
    dispatcher.add_handler(conv_handler)

    # Inicia o bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
