from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import logging
import sys

logging.basicConfig(
    stream = sys.stdout,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)
logger = logging.getLogger(__name__)


TOKEN = '7751960511:AAHLrDZD_5oW2Td9MleAh_HnSMg5-ljzLTo'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    web_app = WebAppInfo(url='https://js13kgames.com/games/offline-paradise')
    webapp_button = KeyboardButton(
        text="Open Web App",
        web_app=web_app
    )
    keyboard = ReplyKeyboardMarkup(
    keyboard=[[webapp_button]],
    resize_keyboard=True,
    one_time_keyboard=True
    )
    await update.message.reply_text(
        "Please choose an option:",
        reply_markup=keyboard
    )

async def handle_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text  
    
    await update.message.reply_text(
        f"You selected: {user_choice}",
        reply_markup=ReplyKeyboardRemove()  # Remove the keyboard
    )




def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start))

    # keyboard answer selection handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_selection))

    app.run_polling()

if __name__ == '__main__':
    main()
