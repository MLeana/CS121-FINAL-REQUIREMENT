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

def json_get_utc(user):
    user = str(user)
    with open("data.json", "r") as file:
        content = json.load(file)
        return content["users"][user]["utc"]


def json_get_info(user):
    user = str(user)
    with open("data.json", "r") as file:
        content = json.load(file)
        return content["users"][user]["reminders"][0]


def json_add_reminder(user):
    user = str(user)
    with open("data.json", "r+") as file:
        content = json.load(file)
        content["users"][user]["reminders"].insert(
            0, {"title": "", "date": "", "time": "", "info": ""}
        )
        file.seek(0)
        json.dump(content, file)
        file.truncate()


def json_add_reminder_info(user, key, value):
    user = str(user)
    key = str(key)
    with open("data.json", "r+") as file:
        content = json.load(file)
        content["users"][user]["reminders"][0][key] = value
        file.seek(0)
        json.dump(content, file)
        file.truncate()


def json_cancel_add_reminder_process(user):
    user = str(user)
    with open("data.json", "r+") as file:
        content = json.load(file)
        del content["users"][user]["reminders"][0]
        file.seek(0)
        json.dump(content, file)
        file.truncate()


def json_delete_reminder(user, index):
    user = str(user)
    index = index - 1

    with open("data.json", "r+") as file:
        content = json.load(file)

        del content["users"][user]["reminders"][index]
        file.seek(0)
        json.dump(content, file)
        file.truncate()


def json_get_reminders_list(user):
    user = str(user)
    with open("data.json", "r+") as file:
        content = json.load(file)
        content = content["users"][user]["reminders"]

        if len(content) == 0:
            message = "📪 You have no reminders!"
            return message

        else:
            message = ""
            for i in range(len(content)):
                title = content[i]["title"]
                date = content[i]["date"]
                time = content[i]["time"]
                info = content[i]["info"]

                message += f"""
*Reminder {i+1}*
------------------
_Title_ : {title}
_Date_ : {date}
_Time_ : {time}
_Info_ : {info}
"""
            return message

        
def start_command(update, context):
    update.message.reply_text(
        "👋 Welcome to my bot! It can remind you of anything in time!",
        reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True),
    )

    new_user = is_new_user(
        update.message.from_user.id,
        update.message.from_user.username,
        update.message.from_user.first_name,
        update.message.from_user.last_name,
    )

    if new_user is True:
        update.message.reply_text(
            "‼ Set your timezone ‼\n\n"
            "Send me your UTC (exp: +2, -1)\n\n"
            "You can always change it later",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ADD_UTC
    else:
        pass


def request_utc(update, context):
    update.message.reply_text(
        "🌐 Please send me your UTC\n\n👉 exemple: +2, -1",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ADD_UTC


def add_utc(update, context):
    utc = str(update.message.text)

    try:
        utc = int(utc)
        json_add_utc(update.message.from_user.id, utc)
        update.message.reply_text(
            "✅ Your timezone was successfully set",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True),
        )
        return ConversationHandler.END
    except:
        update.message.reply_text("❌ Wrong format, please send again")
        return ADD_UTC
    
    def donate(update, context):
    update.message.reply_text(
        "Thank you for donating! ❤",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Buy Me A Coffee", "https://www.buymeacoffee.com/simonfarah"
                    )
                ]
            ]
        ),
    )


def all_reminders(update, context):
    update.message.reply_text(
        f"{json_get_reminders_list(update.message.from_user.id)}", parse_mode="Markdown"
    )


def add_reminder(update, context):
    """Starts the conversation and asks the user about the reminder title."""
    update.message.reply_text(
        "⚡ Adding a new reminder\n\n" "Send /cancel to stop the process.",
        reply_markup=ReplyKeyboardRemove(),
    )

    json_add_reminder(update.message.from_user.id)

    update.message.reply_text("💡 Reminder title :")

    return REMINDER_TITLE
def add_reminder_title(update, context):
    """Stores the reminder title and asks for a reminder date."""
    json_add_reminder_info(update.message.from_user.id, "title", update.message.text)

    update.message.reply_text("📅 Reminder date :\n\nFormat : dd/mm/yyyy")

    return REMINDER_DATE


def add_reminder_date(update, context):
    """Stores the reminder date and asks for a reminder time."""
    json_add_reminder_info(update.message.from_user.id, "date", update.message.text)

    update.message.reply_text("⏲ Reminder time :\n\nFormat : HH:MM AM/PM")

    return REMINDER_TIME


def add_reminder_time(update, context):
    """Stores the reminder time and asks for a reminder info."""
    json_add_reminder_info(update.message.from_user.id, "time", update.message.text)

    update.message.reply_text("ℹ Reminder info :")

    return REMINDER_INFO


def add_reminder_info(update, context):
    """Stores reminder info and ends the conversation."""
    json_add_reminder_info(update.message.from_user.id, "info", update.message.text)

    all_info = json_get_info(update.message.from_user.id)
    reminder_title, reminder_date, reminder_time, reminder_info = (
        all_info["title"],
        all_info["date"],
        all_info["time"],
        all_info["info"],
    )

    utc = json_get_utc(update.message.from_user.id)
    user = update.message.chat_id

    try:
        hours, minutes, m = (
            int(reminder_time.split(" ")[0].split(":")[0]),
            int(reminder_time.split(" ")[0].split(":")[1]),
            reminder_time.split(" ")[1],
        )

    except:
        update.message.reply_text(
            "❌ Wrong time format! We're sorry, you'll have to restart the process...",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True),
        )
        json_cancel_add_reminder_process(update.message.from_user.id)

        return ConversationHandler.END

    if "pm" in m.lower():
        hours = hours + 12
