# sele_sira_bot/bot/utils/constants.py
from telegram.ext import ConversationHandler

ASK_NAME, ASK_PROFESSION, ASK_PHONE, ASK_LOCATION, ASK_ROLE = range(5)

POSTJOB_EMPLOYER, POSTJOB_TITLE, POSTJOB_TYPE, POSTJOB_LOCATION, POSTJOB_SALARY, POSTJOB_DEADLINE, POSTJOB_DESCRIPTION, POSTJOB_CONFIRM = range(5, 13)

ROLES = {
    "role_basic": "basic",
    "role_standard": "standard",
    "role_premium": "premium"
}
