import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from service.ai_agent import AIAgent
from telegram.constants import ParseMode
from telegram.request import HTTPXRequest

# 1. Load Secure Environment Variables
load_dotenv()

# 2. Enable strict logging for security audits
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='telegram_bot_audit.log'
)

# 3. Initialize the Core AI Architecture
agent = AIAgent()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    UX Feature: The Welcome Menu
    Instead of forcing the SME owner to type, we provide 1-click templates.
    """
    welcome_text = (
        "👋 Hello! I am your AI Business Assistant.\n"
        "What would you like to analyze today?"
    )

    # Create interactive buttons linked to our SQL_TEMPLATES
    keyboard = [
        [InlineKeyboardButton("Today's Revenue", callback_data='daily_revenue')],
        [InlineKeyboardButton("This Month's Performance", callback_data='current_month_revenue')],
        [InlineKeyboardButton("Top Selling Categories", callback_data='top_category')],
        [InlineKeyboardButton("Top Product", callback_data='top_quantity_product')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def process_user_request(update: Update, context: ContextTypes.DEFAULT_TYPE, user_text: str):
    """
    Core engine to handle text, fetch DB data, draw charts, and write insights.
    """
    chat_id = update.effective_chat.id

    # UX Feature: Show "typing..." indicator while AI processes
    await context.bot.send_chat_action(chat_id=chat_id, action='typing')

    try:
        # Pass the query to our PromptManager & AI Agent
        insight, chart_path = agent.process_query(user_text)
        # LLM generate bold text with **, while Telegram's Markdown recognize bold text with *
        if isinstance(insight, list):
            insight = insight[0].get("text")

        insight = insight.replace('* ', ' ').replace("**", "*").replace(".", "\.").replace("-", "\-").strip()

        logging.info(insight)

        # 1. Send the Visual Data (Chart)
        if chart_path and os.path.exists(chart_path):
            with open(chart_path, 'rb') as photo:
                await context.bot.send_photo(chat_id=chat_id, photo=photo)

        # 2. Send the Actionable Business Insight
        await context.bot.send_message(chat_id=chat_id, text=insight, parse_mode="MarkdownV2")

    except Exception as e:
        logging.error(f"Execution Error: {str(e)}")
        error_msg = "⚠️ I encountered an error retrieving your data."
        await context.bot.send_message(chat_id=chat_id, text=error_msg)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fallback handler for custom typed ad-hoc queries."""
    user_text = update.message.text
    await process_user_request(update, context, user_text)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for when the user clicks an interactive button."""
    query = update.callback_query
    await query.answer()  # Acknowledge the click immediately

    # Map the button click to a natural language phrase for the Gemini Router
    action_map = {
        'daily_revenue': "Calculate the daily revenue.",
        'current_month_revenue': "Calculate the current month's revenue.",
        'top_category': "Show me the top categories.",
        'top_product': "Show me the top product"
    }

    user_text = action_map.get(query.data, "Show me a general overview.")

    # Notify the user that the request is processing
    await query.message.reply_text(f"🔍 Analyzing: {user_text}")
    await process_user_request(update, context, query.data)


def main():
    """Application Entry Point"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logging.error("CRITICAL: TELEGRAM_BOT_TOKEN missing from .env")
        return

    # Increase the read timeout
    time_request = HTTPXRequest(connection_pool_size=8, read_timeout=60.0)


    application = Application.builder().token(token).request(time_request).build()

    # Route different types of user interactions
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Secure Telegram AI Agent is running...")
    application.run_polling()


if __name__ == '__main__':
    main()