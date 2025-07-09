from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
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
    reply_keyboard = [['Option 1', 'Option 2'], ['Option 3', 'Option 4']]
    
    await update.message.reply_text(
        "Please choose an option:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            resize_keyboard=True, 
            one_time_keyboard=True 
        )
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
