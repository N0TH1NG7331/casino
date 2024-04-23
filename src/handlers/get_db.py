from configs import BOT as bot, ADMIN_IDS
from utils.database import DataBase, UserType
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TRIGGER = "get_db"

async def handler(message):
	success = False

	for admin_id in ADMIN_IDS:
		if message.from_user.id == admin_id:
			success = True
			break

	if not success:
		return

	with open("data/users.db", "rb") as file:
		await bot.send_document(message.from_user.id, file)