from configs import BOT as bot
from utils.database import DataBase, UserType
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TRIGGER = "callback__profile"

def keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("💳 Вывести реферальный баланс", callback_data="callback__withdrawal_referral_balance"),
               InlineKeyboardButton("🔙 Назад", callback_data="callback__main_menu"))
    
    return markup

async def callback(calldata):
    database = DataBase()
    database.open()
    
    if not database.exists_user(calldata.from_user.id):
        referral_id = 0
        database.register_user(calldata.from_user.id, calldata.from_user.username, calldata.from_user.first_name, referral_id)
        
        
    me = await bot.get_me()
    data = database.find_user_by_id(calldata.from_user.id)
    
    await bot.edit_message_text(f"""
<b>Ваш профиль:</b>

<b>👁‍🗨 ID:</b> <code>{calldata.from_user.id}</code>
<b>🔗 Ссылка для друга:</b> <code>t.me/{me.username}?start={calldata.from_user.id}</code>
<b>💷 Реферальный баланс:</b> <code>{data[UserType.referral_balance]} USDT</code>

<b>🏆 Побед:</b> <code>{data[UserType.victories]}</code>
<b>❌ Проигрышей:</b> <code>{data[UserType.losses]}</code>
    	""", calldata.message.chat.id, calldata.message.id, reply_markup=keyboard())
    
    database.close()