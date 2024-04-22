from configs import BOT as bot
from utils.database import DataBase
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

async def callback(calldata):
    coin = calldata.data.split("-")[1]
    database = DataBase()
    database.open()
    database.execute(f"""UPDATE users SET `pay_wait_count` = 1 WHERE user_id = {calldata.from_user.id}""")
    database.commit()
    database.execute(f"""UPDATE users SET `pay_asset` = '{coin}' WHERE user_id = {calldata.from_user.id}""")
    database.commit()
    database.close()
    
    min_bet = "0.001" if coin == "TON" else "0.1"
    
    await bot.edit_message_text(f"""<b>Введите сумму ставки!</b>⚡️

<b>Минимальная ставка:</b> <code>{min_bet} {coin}</code>
<blockquote><i>(вводите только число!)</i></blockquote>""", calldata.message.chat.id, calldata.message.id)
    