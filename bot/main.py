# sele_sira_bot/bot/main.py
from telegram.ext import ApplicationBuilder
from config.settings import BOT_TOKEN
from bot.handlers.start import registration_handler, options_callback_handler
from bot.handlers.post_job import post_job_conversation
from db.models import Base
from db.db import engine

# Create DB tables
Base.metadata.create_all(bind=engine)

if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN is not set. Please check your .env file.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(registration_handler)
app.add_handler(options_callback_handler)
app.add_handler(post_job_conversation)

if __name__ == '__main__':
    app.run_polling()
