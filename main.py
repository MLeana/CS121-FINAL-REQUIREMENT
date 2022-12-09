import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
)

load_dotenv()

main_keyboard = [
    ["➕ Add Reminder", "➖ Delete History"],
    ["📃 All Reminders", "🌐 Change UTC"],
    ["💰 Donate"],
]

REMINDER_TITLE, REMINDER_DATE, REMINDER_TIME, REMINDER_INFO = range(4)
DELETE_REMINDER_INDEX = range(1)
ADD_UTC = range(1)
