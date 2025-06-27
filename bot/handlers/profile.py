from telegram import Update
from telegram.ext import CallbackContext

async def handle_profile(update: Update, context: CallbackContext):
    """Handle the 'Profile' option from the main menu."""
    query = update.callback_query
    await query.edit_message_text("Welcome to your Profile! (Feature coming soon)")
