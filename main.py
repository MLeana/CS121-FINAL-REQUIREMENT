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

def is_new_user(user, username, first_name, last_name):
    user = str(user)
    with open("data.json", "r+") as file:
        content = json.load(file)
        if user not in content["users"]:
            content["users"][user] = {
                "username": username,
                "first name": first_name,
                "last name": last_name,
                "utc": "",
                "reminders": [],
            }
            file.seek(0)
            json.dump(content, file)
            file.truncate()

            return True
        else:
            return False


def json_add_utc(user, utc):
    user = str(user)
    with open("data.json", "r+") as file:
        content = json.load(file)
        content["users"][user]["utc"] = utc
        file.seek(0)
        json.dump(content, file)
        file.truncate()
