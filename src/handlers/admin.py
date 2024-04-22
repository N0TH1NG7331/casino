from configs import BOT as bot, ADMIN_IDS
from utils.database import DataBase, UserType
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TRIGGER = "admin"

async def handler(message):
	success = False

	for admin_id in ADMIN_IDS:
		if message.from_user.id == admin_id:
			success = True
			break

	if not success:
		return

	# markup = 

	await bot.send_message(message.from_user.id, f"Добро пожаловать, {message.from_user.id}")