from configs import BOT as bot, CRYPTOPAY  as cryptopay, ADMIN_IDS
from utils.database import DataBase, UserType
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TRIGGER = "callback__withdrawal_referral_balance"

# SELECT referral_balance FROM users WHERE user_id = 

async def callback(calldata):
    database = DataBase()
    database.open()
    
    if not database.exists_user(calldata.from_user.id):
        referral_id = 0
        database.register_user(calldata.from_user.id, calldata.from_user.username, calldata.from_user.first_name, referral_id)
    
    user = database.find_user_by_id(calldata.from_user.id)
    referral_balance = float(user[UserType.referral_balance])

    if referral_balance < 1.5:
        await bot.answer_callback_query(calldata.id, "Минимальные средства для вывода 1.5 USDT")
        return
    
    print(f"[DEBUG] User: {calldata.from_user.id} withdrawel: {referral_balance}")
    check = cryptopay.createCheck("USDT", str(referral_balance), {"pin_to_user_id": calldata.from_user.id})
    if check['ok'] == False:
        if check['error']['name'] == "NOT_ENOUGH_COINS":
            print(f"[WARNING] Error withdrawel amount {referral_balance} by {calldata.from_user.id} | {calldata.from_user.first_name} | {calldata.from_user.username}")
            
            balance = cryptopay.getBalance()
            
            for admin_id in ADMIN_IDS:
                await bot.send_message(admin_id, f"""
❗️ <b>Ошибка при выводе реферального баланса</b> ❗️
👤 <b>Игрок:</b> <code>{calldata.from_user.id}</code> {f'<code>{calldata.from_user.first_name}</code>' if calldata.from_user.username else ''}
💰 <b>Сумма вывода:</b> <code>{referral_balance}</code>
💸 <b>Доступный баланс</b> <code>{balance["result"][0]["available"]} USDT | {balance["result"][1]["available"]} TON</code>💲
""")
            
            await bot.send_message(calldata.from_user.id, "Ошибка, недостаточно средств на балансе")
            return
    
    await bot.send_message(calldata.from_user.id, f"🔗 <b>Ссылка для получение средств: </b>{check['result']['bot_check_url']}")
    referral_balance = 0
    
    database.execute(f'''UPDATE users SET referral_balance = '{str(referral_balance)}' WHERE user_id = {calldata.from_user.id}''')
    database.commit()
    
    database.close()