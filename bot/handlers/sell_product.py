from telegram import Update
from telegram.ext import CallbackContext

async def handle_sell_product(update: Update, context: CallbackContext):
    """Handle the 'Sell Product' option from the main menu."""
    query = update.callback_query
    await query.edit_message_text("Welcome to the Sell Product section! (Feature coming soon)")
