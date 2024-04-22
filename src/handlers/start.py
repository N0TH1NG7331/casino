from configs import BOT as bot
from utils.database import DataBase, UserType
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TRIGGER = "start"

def keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🕹 Играть", callback_data="callback__start_game"),
               InlineKeyboardButton("👤 Профиль", callback_data="callback__profile"))
    
    return markup

async def handler(message):
    database = DataBase()
    database.open()
    
    if not database.exists_user(message.from_user.id):
        try:
            referral_id = int(message.text.split(" ")[1])
        except:
            referral_id = 0
        database.register_user(message.from_user.id, message.from_user.username, message.from_user.first_name, referral_id)

    data = database.find_user_by_id(message.from_user.id)
    if data[UserType.pay_started] == 1:
        database.reset_pay(message.from_user.id)
    database.close()
    
    await bot.send_message(message.from_user.id, f"🙋 Добро пожаловать <b>{message.from_user.first_name}</b> в <b>MaxBet Казино</b>", reply_markup=keyboard())