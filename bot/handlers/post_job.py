from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters
from db.models import Job
from db.db import SessionLocal
from bot.utils.formatter import get_translation
from bot.utils.constants import (
    POSTJOB_EMPLOYER, POSTJOB_TITLE, POSTJOB_TYPE, POSTJOB_LOCATION, POSTJOB_SALARY, POSTJOB_DEADLINE, POSTJOB_DESCRIPTION, POSTJOB_CONFIRM
)


async def handle_post_job(update: Update, context: CallbackContext):
    """Start the post job conversation."""
    query = update.callback_query
    await query.edit_message_text(get_translation(context.user_data.get('lang', 'en'))["postjob_employer"])
    return POSTJOB_EMPLOYER


async def postjob_employer(update: Update, context: CallbackContext):
    context.user_data['postjob_employer'] = update.message.text
    await update.message.reply_text(get_translation(context.user_data.get('lang', 'en'))["postjob_title"])
    return POSTJOB_TITLE


async def postjob_title(update: Update, context: CallbackContext):
    context.user_data['postjob_title'] = update.message.text
    await update.message.reply_text(get_translation(context.user_data.get('lang', 'en'))["postjob_type"])
    return POSTJOB_TYPE


async def postjob_type(update: Update, context: CallbackContext):
    context.user_data['postjob_type'] = update.message.text
    await update.message.reply_text(get_translation(context.user_data.get('lang', 'en'))["postjob_location"])
    return POSTJOB_LOCATION


async def postjob_location(update: Update, context: CallbackContext):
    context.user_data['postjob_location'] = update.message.text
    await update.message.reply_text(get_translation(context.user_data.get('lang', 'en'))["postjob_salary"])
    return POSTJOB_SALARY


async def postjob_salary(update: Update, context: CallbackContext):
    context.user_data['postjob_salary'] = update.message.text
    await update.message.reply_text(get_translation(context.user_data.get('lang', 'en'))["postjob_deadline"])
    return POSTJOB_DEADLINE


async def postjob_deadline(update: Update, context: CallbackContext):
    context.user_data['postjob_deadline'] = update.message.text
    await update.message.reply_text(get_translation(context.user_data.get('lang', 'en'))["postjob_description"])
    return POSTJOB_DESCRIPTION


async def postjob_description(update: Update, context: CallbackContext):
    context.user_data['postjob_description'] = update.message.text
    # Show confirmation
    summary = (
        f"<b>Employer:</b> {context.user_data['postjob_employer']}\n"
        f"<b>Job Title:</b> {context.user_data['postjob_title']}\n"
        f"<b>Type:</b> {context.user_data['postjob_type']}\n"
        f"<b>Location:</b> {context.user_data['postjob_location']}\n"
        f"<b>Salary:</b> {context.user_data['postjob_salary']}\n"
        f"<b>Deadline:</b> {context.user_data['postjob_deadline']}\n"
        f"<b>Description:</b> {context.user_data['postjob_description']}\n"
    )
    await update.message.reply_text(
        get_translation(context.user_data.get('lang', 'en'))["postjob_confirm"] + f"\n\n{summary}",
        parse_mode='HTML'
    )
    return POSTJOB_CONFIRM


async def postjob_confirm(update: Update, context: CallbackContext):
    text = update.message.text.strip().lower()
    if text == 'confirm':
        # Save to DB
        session = SessionLocal()
        job = Job(
            employer_name=context.user_data['postjob_employer'],
            job_title=context.user_data['postjob_title'],
            job_type=context.user_data['postjob_type'],
            location=context.user_data['postjob_location'],
            salary=context.user_data['postjob_salary'],
            deadline=context.user_data['postjob_deadline'],
            description=context.user_data['postjob_description'],
        )
        session.add(job)
        session.commit()
        session.close()
        await update.message.reply_text(get_translation(context.user_data.get('lang', 'en'))["postjob_success"])
        return ConversationHandler.END
    else:
        await update.message.reply_text("❌ Please type 'confirm' to post the job or restart to edit.")
        return POSTJOB_CONFIRM


post_job_conversation = ConversationHandler(
    entry_points=[CommandHandler('postjob', handle_post_job)],
    states={
        POSTJOB_EMPLOYER: [MessageHandler(filters.TEXT & ~filters.COMMAND, postjob_employer)],
        POSTJOB_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, postjob_title)],
        POSTJOB_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, postjob_type)],
        POSTJOB_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, postjob_location)],
        POSTJOB_SALARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, postjob_salary)],
        POSTJOB_DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, postjob_deadline)],
        POSTJOB_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, postjob_description)],
        POSTJOB_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, postjob_confirm)],
    },
    fallbacks=[],
)
