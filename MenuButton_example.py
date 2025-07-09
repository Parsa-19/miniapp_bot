from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, LoginUrl
from telegram import Update, BotCommand, MenuButtonCommands, MenuButton, MenuButtonWebApp
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging
import sys

logging.basicConfig(
    stream = sys.stdout,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = '7751960511:AAHLrDZD_5oW2Td9MleAh_HnSMg5-ljzLTo'

# Define commands
COMMANDS = [
    BotCommand(command="start", description="Start the bot"),
    BotCommand(command="help", description="Get help using the bot"),
    BotCommand(command="about", description="Learn more about this bot"),
]




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your Menu Bot. Use the menu button to explore commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a sample bot with a custom menu using MenuButton.")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Created with ❤️ using python-telegram-bot.")

async def set_webapp_menu_button(application):
    """Set the custom menu button with predefined commands."""
    await application.bot.set_my_commands(COMMANDS)
    await application.bot.set_chat_menu_button(menu_button=MenuButtonCommands())
    await application.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Open WebApp", web_app=WebAppInfo(url='https://js13kgames.com/games/offline-paradise'))
    )



def main():
    app = Application.builder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))

    async def post_init(application: Application):
        await set_webapp_menu_button(application)

    app.post_init = post_init  # Assign the async function

    app.run_polling()

if __name__ == "__main__":
    main()


