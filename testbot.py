from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo, LoginUrl
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

import logging
import sys

logging.basicConfig(
	stream = sys.stdout,
	format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level = logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = '7751960511:AAHLrDZD_5oW2Td9MleAh_HnSMg5-ljzLTo'

START_MESSAGE = '''
the bot is started now.
press buttons below:
'''

HELP_MESSAGE = '''
available commands are:
/start
/help
'''


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	logger.info(f'bot started by user with id: {update.effective_user.id}')

	keyboard = [
		[
			InlineKeyboardButton('Button ONE data=111', callback_data='111'),
			InlineKeyboardButton('Button TWO data=222', callback_data='222'),
		],
		[
			InlineKeyboardButton('Button THREE data=333', callback_data='333'),
			InlineKeyboardButton('Button FOUR data=444', callback_data='444'),

		],
		[
			InlineKeyboardButton('Button FIVE data=555', callback_data='555'),
		], 
		[
			InlineKeyboardButton('SIX = 666', callback_data='666'),
			InlineKeyboardButton('SEVEN = 777', callback_data='777'),
			InlineKeyboardButton('EIGHT = 888', callback_data='888'),
		]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	await update.message.reply_text(START_MESSAGE, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	logger.info(f'requested help by user id: {update.effective_user.id}')
	await update.message.reply_text(HELP_MESSAGE)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	logger.info('button handler started..')
	query = update.callback_query
	await query.answer()
	await query.edit_message_text(text=f"Selected option: {query.data}")



def main():
	app = ApplicationBuilder().token(TOKEN).build()

	# commands
	app.add_handler(CommandHandler('start', start_command))
	app.add_handler(CommandHandler('help', help_command))

	# buttons
	app.add_handler(CallbackQueryHandler(button_handler))

	app.run_polling()

if __name__ == '__main__':
	main()
