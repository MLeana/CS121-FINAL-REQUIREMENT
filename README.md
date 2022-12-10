# TELEGRAM REMINDER BOT

### FEATURES OF TELEGRAM REMINDER BOT

  What can this Telegram Bot do?
  1. Remind a user of event with specific time and date.
  2. Make a conversation with a user to add reminders.
  3. Save a user reminder history.
  4. Let a user delete a reminder from history.

### In this version
  1. Install the required modules.
  2. Create a Bot on Telegram and gets it's API Token.
  3. Setting up the main functions. 
  4. Create our Main Menu and variables.
  5. Create functions to save the data.
  6. Handle messages and conversations with the telegram Bot using Python.
  7. Telling the bot what functions to use
  8. Run the BOT!

### Required Modules/Dependencies
  1. Python-Telegram-Module
  2. Pip.
  3. Python-dotenv

```mermaid
journey
	title UML Diagram for Bejeweled Bot
	section User open the Bot
		User press start: 5: User
		Bot replies introduction: 5: Bot
		Bot asks for an action: 5: Bot
		User chooses Change UTC: 5: User
    Bot changes timezone: 5: Bot
    Bot asks for another action: 5: Bot
    User chooses Add Reminder: 5: User
    Bot asks for Reminder Title, Reminder Date, Reminder Time and Reminder info: 5: Bot
    User answers all questions: 5: User
	section Other Options
		All Reminders: 5: Bot
		Delete History: 5: Bot
	section Result Declared
		Reminder Succesfully Added: 5: Bot
		Reminder Deleted Succesfully: 5: Bot
    Wrong time format! We're sorry, you'll have to restart the process...: 1: Bot
    Wrong date format! We're sorry, you'll have to restart the process...: 1: Bot    
```
