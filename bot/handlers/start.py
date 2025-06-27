# sele_sira_bot/bot/handlers/start.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from db.models import User
from db.db import SessionLocal
from bot.utils.formatter import get_translation
from bot.utils.constants import (
    ASK_NAME,
    ASK_PROFESSION,
    ASK_PHONE,
    ASK_LOCATION,
    ASK_ROLE,
    ROLES,
)
from bot.handlers.sell_product import handle_sell_product
from bot.handlers.post_job import handle_post_job, post_job_conversation
from bot.handlers.promote_self import handle_promote_self
from bot.handlers.profile import handle_profile


async def start(update: Update, context: CallbackContext):
    """Handle the /start command and begin the registration process."""
    lang = 'en'  # Or detect based on user
    context.user_data['lang'] = lang
    strings = get_translation(lang)
    if update.message:
        await update.message.reply_text(strings["welcome"])
        await update.message.reply_text(strings["ask_name"])
        return ASK_NAME
    else:
        return ConversationHandler.END


async def ask_name(update: Update, context: CallbackContext):
    """Handle the user's name input during registration."""
    if update.message and update.message.text:
        context.user_data['name'] = update.message.text
        await update.message.reply_text(
            get_translation(context.user_data['lang'])["ask_profession"]
        )
        return ASK_PROFESSION
    else:
        return ConversationHandler.END


async def ask_profession(update: Update, context: CallbackContext):
    """Handle the user's profession input during registration."""
    if update.message and update.message.text:
        context.user_data['profession'] = update.message.text
        await update.message.reply_text(
            get_translation(context.user_data['lang'])["ask_phone"]
        )
        return ASK_PHONE
    else:
        return ConversationHandler.END


async def ask_phone(update: Update, context: CallbackContext):
    """Handle the user's phone input during registration."""
    if update.message and update.message.text:
        context.user_data['phone'] = update.message.text
        await update.message.reply_text(
            get_translation(context.user_data['lang'])["ask_location"]
        )
        return ASK_LOCATION
    else:
        return ConversationHandler.END


async def ask_location(update: Update, context: CallbackContext):
    """Handle the user's location input during registration."""
    if update.message and update.message.text:
        context.user_data['location'] = update.message.text
        strings = get_translation(context.user_data['lang'])
        keyboard = [
            [InlineKeyboardButton(strings["roles"]["basic"], callback_data="role_basic")],
            [InlineKeyboardButton(strings["roles"]["standard"], callback_data="role_standard")],
            [InlineKeyboardButton(strings["roles"]["premium"], callback_data="role_premium")],
        ]
        await update.message.reply_text(
            strings["ask_role"], reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return ASK_ROLE
    else:
        return ConversationHandler.END


async def ask_role(update: Update, context: CallbackContext):
    """Handle the user's role selection and save registration data to the database."""
    query = update.callback_query
    await query.answer()
    role = ROLES.get(query.data, "basic")
    context.user_data['role'] = role
    strings = get_translation(context.user_data['lang'])

    # Save user to DB
    session = SessionLocal()
    user = User(
        telegram_id=query.from_user.id,
        full_name=context.user_data['name'],
        profession=context.user_data['profession'],
        phone=context.user_data['phone'],
        location=context.user_data['location'],
        language=context.user_data['lang'],
        role=role
    )
    session.add(user)
    session.commit()
    session.close()

    await query.edit_message_text(strings["registered"])

    # Send options keyboard
    options_keyboard = [
        [InlineKeyboardButton("Market Myself (Company)", callback_data="option_market_myself")],
        [InlineKeyboardButton("Post Job", callback_data="option_post_job")],
        [InlineKeyboardButton("Sell Product", callback_data="option_sell_product")],
        [InlineKeyboardButton("Profile", callback_data="option_profile")],
    ]
    await query.message.reply_text(
        "What would you like to do next?",
        reply_markup=InlineKeyboardMarkup(options_keyboard)
    )
    return ConversationHandler.END


async def options_handler(update: Update, context: CallbackContext):
    """Handle the user's selection from the main options keyboard."""
    query = update.callback_query
    await query.answer()
    option = query.data
    if option == "option_market_myself":
        await handle_promote_self(update, context)
    elif option == "option_post_job":
        await handle_post_job(update, context)
        return  # Do not continue, as handle_post_job starts a conversation
    elif option == "option_sell_product":
        await handle_sell_product(update, context)
    elif option == "option_profile":
        await handle_profile(update, context)
    else:
        await query.edit_message_text("Unknown option selected.")

registration_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
        ASK_PROFESSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_profession)],
        ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
        ASK_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_location)],
        ASK_ROLE: [CallbackQueryHandler(ask_role)],
    },
    fallbacks=[],
)

# Add a global handler for the options keyboard
options_callback_handler = CallbackQueryHandler(options_handler, pattern=r"^option_")
