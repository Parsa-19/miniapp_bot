from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import logging
import sys

logging.basicConfig(
	stream = sys.stdout,
	format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level = logging.INFO
)
logger = logging.getLogger(__name__)

MINI_APP_URL = r'https://js13kgames.com/games/offline-paradise'
IMAGE_PATH = 'plus_logo.jpeg'

TOKEN = '7751960511:AAHLrDZD_5oW2Td9MleAh_HnSMg5-ljzLTo'

START_MESSAGE = '''
hey there!
this bot is to lunch a mini app and currently is under the develpment.
try the /help command to see all commands for this bot.
lunch the mini app by the way with button below.
'''
HELP_MESSAGE = '''
you can use these commands to use the bot
/start
/help
'''



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	logger.info(f'User {update.effective_user.id} started the bot')
	keyboard = [
		[InlineKeyboardButton(
			"Start game mini app",
			web_app = {'url': MINI_APP_URL}
			)]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	try:
		with open(IMAGE_PATH, 'rb') as image:
			await update.message.reply_photo(
				photo = image,
				caption = START_MESSAGE,
				reply_markup = reply_markup 
			)
	except FileNotFoundError:
		logger.error(f'plus logo image not found at {IMAGE_PATH}')
		await update.message.replay_text(
			START_MESSAGE, 
			reply_markup = reply_markup
		)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	logger.info(f'User {update.effective_user.id} requested help command')
	await update.message.reply_text(HELP_MESSAGE)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	logger.error('Exception while handling an update:', exc_info = context.error)
	if update and update.effective_message:
		await update.effective_message.reply_text(
			'sorry, there is a error accured in bot plz try agian later...'
		)


async def signal_handler(signum, frame):
	logger.info(f'Signal recieved, shutting down the bot..')
	exit(0)


if __name__ == '__main__':

	app = ApplicationBuilder().token(TOKEN).build()

	app.add_handler(CommandHandler('start', start_command))
	app.add_handler(CommandHandler('help', help_command))

	app.add_error_handler(error_handler)

	app.run_polling()