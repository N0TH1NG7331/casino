from configs import BOT as bot
from utils.database import DataBase, UserType
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TRIGGER = "callback__main_menu"

def keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🕹 Играть", callback_data="callback__start_game"),
               InlineKeyboardButton("👤 Профиль", callback_data="callback__profile"))
    
    return markup

async def callback(calldata):
    database = DataBase()
    database.open()
    
    if not database.exists_user(calldata.from_user.id):
        database.register_user(calldata.from_user.id, calldata.from_user.username, calldata.from_user.first_name)

    data = database.find_user_by_id(calldata.from_user.id)
    if data[UserType.pay_started] == 1:
        database.reset_pay(calldata.from_user.id)
    database.close()


    
    await bot.edit_message_text(f"🙋 Добро пожаловать <b>{calldata.from_user.first_name}</b> в <b>MaxBet Казино</b>", calldata.message.chat.id,
                                calldata.message.id, reply_markup=keyboard())