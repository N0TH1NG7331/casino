from configs import BOT as bot
from utils.database import DataBase, UserType
from telebot import types

async def printer(calldata):
    database = DataBase()
    database.open()
    data = database.find_user_by_id(calldata.from_user.id)
    database.close()

    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("💲USDT", callback_data="callback__coin-USDT"),
               types.InlineKeyboardButton("💎TON", callback_data="callback__coin-TON"))
    markup.row(types.InlineKeyboardButton("🔙 Назад", callback_data=f"callback__game-{data[UserType.game]}"))
    await bot.edit_message_text(f"<b>💸Выберите монету для оплаты!</b>",
                                calldata.message.chat.id, calldata.message.id, reply_markup=markup)

async def callback(calldata):
    database = DataBase()
    database.open()
    database.execute(f'''UPDATE users SET game_bet_to_win = '{calldata.data.split("-")[1]}' WHERE user_id = {calldata.from_user.id}''')
    database.commit()
    database.close()
    
    await printer(calldata)