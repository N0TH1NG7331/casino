from configs import BOT as bot
from utils.database import DataBase
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def cube_bet_keyboards():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("📈 Больше", callback_data="callback__cube-more"),
               InlineKeyboardButton("📉 Меньше", callback_data="callback__cube-less"))
    markup.row(InlineKeyboardButton("👍 Чёт", callback_data="callback__cube-even"),
               InlineKeyboardButton("👎 Нечет", callback_data="callback__cube-odd"))
    markup.row(InlineKeyboardButton("⚔️ Дуэль", callback_data="callback__cube-duel"),
               InlineKeyboardButton("🎱Плинко", callback_data="callback__cube-plinko"))
    markup.row(InlineKeyboardButton("🔙 Назад", callback_data="callback__start_game"))

    return markup


def bf_bet_keyboards():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("️✔️ Гол", callback_data="callback__bf-hit"),
               InlineKeyboardButton("❌ Промах", callback_data="callback__bf-miss"))
    # markup.row(InlineKeyboardButton("⚔️ Дуэль (Скоро)", callback_data="callback__bf-duel"))
    markup.row(InlineKeyboardButton("🔙 Назад", callback_data="callback__start_game"))

    return markup

def darts_bet_keyboards():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🔴 Красный", callback_data="callback__darts-red"),
               InlineKeyboardButton("️⚪️ Белый", callback_data="callback__darts-white"))
    markup.row(InlineKeyboardButton("💯 Точно в цель", callback_data="callback__darts-hit"),
               InlineKeyboardButton("❌ Промах", callback_data="callback__darts-miss"))
    # markup.row(InlineKeyboardButton("⚔️ Дуэль (Скоро)", callback_data="callback__darts-duel"))
    markup.row(InlineKeyboardButton("🔙 Назад", callback_data="callback__start_game"))

    return markup

def casino_bet_keyboards():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("️🫐 Черника", callback_data="callback__casino-blueberries"),
               InlineKeyboardButton("️ 777", callback_data="callback__casino-777"))
    markup.row(InlineKeyboardButton("◼️ Бар", callback_data="callback__casino-bar"),
               InlineKeyboardButton("🍋 Лимоны", callback_data="callback__casino-lemons"))
    markup.row(InlineKeyboardButton("🔙 Назад", callback_data="callback__start_game"))

    return markup

async def callback_cube(calldata):
    database = DataBase()
    database.open()
    database.execute(f'''UPDATE users SET game = 'cube' WHERE user_id = {calldata.from_user.id}''')
    database.commit()
    database.close()
    
    await bot.edit_message_text("Хорошо, на что ставим?", calldata.message.chat.id, calldata.message.id, reply_markup=cube_bet_keyboards())
     
async def callback_basketball(calldata):
    database = DataBase()
    database.open()
    database.execute(f'''UPDATE users SET game = 'basketball' WHERE user_id = {calldata.from_user.id}''')
    database.commit()
    database.close()
    
    await bot.edit_message_text("Хорошо, на что ставим?", calldata.message.chat.id, calldata.message.id, reply_markup=bf_bet_keyboards())
    
async def callback_football(calldata):
    database = DataBase()
    database.open()
    database.execute(f'''UPDATE users SET game = 'football' WHERE user_id = {calldata.from_user.id}''')
    database.commit()
    database.close()
    
    await bot.edit_message_text("Хорошо, на что ставим?", calldata.message.chat.id, calldata.message.id, reply_markup=bf_bet_keyboards())
    
async def callback_darts(calldata):
    database = DataBase()
    database.open()
    database.execute(f'''UPDATE users SET game = 'darts' WHERE user_id = {calldata.from_user.id}''')
    database.commit()
    database.close()
    
    await bot.edit_message_text("Хорошо, на что ставим?", calldata.message.chat.id, calldata.message.id, reply_markup=darts_bet_keyboards())
    
async def callback_casino(calldata):
    database = DataBase()
    database.open()
    database.execute(f'''UPDATE users SET game = 'casino' WHERE user_id = {calldata.from_user.id}''')
    database.commit()
    database.close()
    
    await bot.edit_message_text("Хорошо, на что ставим?", calldata.message.chat.id, calldata.message.id, reply_markup=casino_bet_keyboards())