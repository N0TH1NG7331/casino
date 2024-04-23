from configs import BOT as bot, ADMIN_IDS, CRYPTOPAY as cryptopay
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

	split = message.text.split(" ")
	check = cryptopay.createCheck("USDT", str(split[0]), {"pin_to_user_id": message.from_user.id})
	
	if check['ok'] == False:
		if check['error']['name'] == "NOT_ENOUGH_COINS":
			await bot.send_message(message.from_user.id, "нету денег соси")

	await bot.send_message(f"на сука деньги: {check['result']['bot_check_url']}")