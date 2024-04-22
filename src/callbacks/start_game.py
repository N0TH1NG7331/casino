from configs import BOT as bot
from utils.database import DataBase
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TRIGGER = "callback__start_game"

def keyboard():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🎲 Кости", callback_data="callback__game-cube"))
    markup.row(InlineKeyboardButton("🏀 Баскетбол", callback_data="callback__game-basketball"))
    markup.row(InlineKeyboardButton("⚽️ Футбол", callback_data="callback__game-football"))
    markup.row(InlineKeyboardButton("🎯 Дартc", callback_data="callback__game-darts"))
    markup.row(InlineKeyboardButton("🎰 Слоты", callback_data="callback__game-casino"))
    markup.row(InlineKeyboardButton("🔙 Назад", callback_data="callback__main_menu"))

    return markup
    

async def callback(calldata):
    database = DataBase()
    database.open()
    database.execute(f'''UPDATE users SET pay_started = 1 WHERE user_id = {calldata.from_user.id}''')
    database.commit()
    database.close()
    
    await bot.edit_message_text("Отлично, во что будем играть?", calldata.message.chat.id, calldata.message.id, reply_markup=keyboard())