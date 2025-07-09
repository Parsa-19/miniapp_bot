import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import json

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token from BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Your web app URL (can be ngrok, your domain, or local server)
WEB_APP_URL = "https://your-domain.com/webapp"  # Replace with your actual URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with inline keyboard containing web app button."""
    
    # Create inline keyboard with web app button
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Open Web App", 
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ],
        [
            InlineKeyboardButton("📱 Mini App", web_app=WebAppInfo(url=f"{WEB_APP_URL}/mini")),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings")
        ],
        [
            InlineKeyboardButton("📊 Dashboard", web_app=WebAppInfo(url=f"{WEB_APP_URL}/dashboard")),
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎯 Welcome to PLUS Web App!\n\n"
        "Choose an option below:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "settings":
        # Create settings keyboard with web app
        keyboard = [
            [
                InlineKeyboardButton(
                    "🔧 Open Settings", 
                    web_app=WebAppInfo(url=f"{WEB_APP_URL}/settings")
                )
            ],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "⚙️ Settings Menu\n\nConfigure your preferences:",
            reply_markup=reply_markup
        )
    
    elif query.data == "help":
        keyboard = [
            [
                InlineKeyboardButton(
                    "📚 Help Center", 
                    web_app=WebAppInfo(url=f"{WEB_APP_URL}/help")
                )
            ],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "❓ Help & Support\n\nGet assistance:",
            reply_markup=reply_markup
        )
    
    elif query.data == "back_to_main":
        # Return to main menu
        keyboard = [
            [
                InlineKeyboardButton(
                    "🚀 Open Web App", 
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ],
            [
                InlineKeyboardButton("📱 Mini App", web_app=WebAppInfo(url=f"{WEB_APP_URL}/mini")),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings")
            ],
            [
                InlineKeyboardButton("📊 Dashboard", web_app=WebAppInfo(url=f"{WEB_APP_URL}/dashboard")),
                InlineKeyboardButton("❓ Help", callback_data="help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🎯 Welcome to PLUS Web App!\n\n"
            "Choose an option below:",
            reply_markup=reply_markup
        )

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle data sent from web app."""
    # This function handles data sent from your web app back to the bot
    web_app_message = update.effective_message.web_app_data
    
    if web_app_message:
        # Parse the data sent from web app
        try:
            data = json.loads(web_app_message.data)
            
            # Process the data based on what your web app sends
            if data.get('action') == 'form_submit':
                await update.message.reply_text(
                    f"✅ Form submitted successfully!\n\n"
                    f"Name: {data.get('name', 'N/A')}\n"
                    f"Email: {data.get('email', 'N/A')}\n"
                    f"Message: {data.get('message', 'N/A')}"
                )
            
            elif data.get('action') == 'settings_update':
                await update.message.reply_text(
                    f"⚙️ Settings updated!\n\n"
                    f"Theme: {data.get('theme', 'default')}\n"
                    f"Notifications: {data.get('notifications', 'enabled')}"
                )
            
            else:
                await update.message.reply_text(
                    f"📦 Data received from web app:\n\n"
                    f"```json\n{json.dumps(data, indent=2)}\n```",
                    parse_mode='MarkdownV2'
                )
                
        except json.JSONDecodeError:
            await update.message.reply_text(
                f"📦 Raw data received: {web_app_message.data}"
            )

async def webapp_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Direct command to open web app."""
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Launch App", 
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌐 Click below to open the web app:",
        reply_markup=reply_markup
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("webapp", webapp_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Handler for web app data
    application.add_handler(
        MessageHandler(
            filters.StatusUpdate.WEB_APP_DATA, 
            web_app_data
        )
    )
    
    # Error handler
    application.add_error_handler(error_handler)

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

# Additional configuration for webhook (if needed)
"""
For webhook setup instead of polling:

from telegram.ext import Updater
import os

def setup_webhook():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Set webhook
    application.bot.set_webhook(
        url=f"https://your-domain.com/webhook/{BOT_TOKEN}",
        allowed_updates=Update.ALL_TYPES
    )
    
    # Add handlers (same as above)
    application.add_handler(CommandHandler("start", start))
    # ... other handlers
    
    # Run with webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        webhook_url=f"https://your-domain.com/webhook/{BOT_TOKEN}"
    )
"""