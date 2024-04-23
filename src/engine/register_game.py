import json
import requests

from .engine import Engine, transform_emoji_name_to_textRU, transform_bet, transform_text_to_emoji
from utils.database import DataBase, UserType
from configs import BOT as bot, CRYPTOPAY as cryptopay, CHANNAL_ID, ADMIN_IDS, TON_USDT, USDT_RUB
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncio import sleep
from handlers.start import keyboard as start_keyboard

def keyboard_to_pay(link):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("💳 Оплатить", url=link))
    
    return markup

async def generate_payment(message, data, bet: float, coin: str) -> bool:
    database = DataBase()
    database.open()
    database.execute(f"""UPDATE users SET pay_wait_count = 0 AND pay_count = '{str(bet)}' WHERE user_id = {message.from_user.id}""")
    database.commit()
    database.close()
    emoji_name = transform_emoji_name_to_textRU(data[UserType.game])
    coin = coin.upper()
    
    print(f"[DEBUG] User ({message.from_user.id} | {message.from_user.first_name}) created check({bet} | {coin}) waiting to pay...")
    pay_check = cryptopay.createInvoice(coin, str(bet), {"expires_in": 300})
    
    msg = await bot.send_message(message.from_user.id, f"""
🧾 <b>Чек: </b>
🆔 <b>ID:</b> <code>{pay_check['result']['invoice_id']}</code>
🕹 <b>Игра:</b> <code>{emoji_name}</code>
💵 <b>Сумма:</b> <code>{str(bet)} {coin}</code>
🔗 <b>Ссылка:</b> {pay_check['result']['bot_invoice_url'].split("https://")[1]}
⏳ <b>Время на оплату:</b> <code>5 минут</code>

📍 Статус: <code>Ожидаем оплаты</code>
""", reply_markup=keyboard_to_pay(pay_check['result']['bot_invoice_url'].split("https://")[1]))
    
    check = cryptopay.getInvoice(coin, pay_check['result']['invoice_id'])
    while check['result']['items'][0]['status'] != "paid":
        if check['result']['items'][0]['status'] == "expired":
            await bot.edit_message_text(f"""🧾 <b>Чек: </b>
🆔 <b>ID:</b> <code>{pay_check['result']['invoice_id']}</code>
🕹 <b>Игра:</b> <code>{emoji_name}</code>
💵 <b>Сумма:</b> <code>{str(bet)} {coin}</code>
🔗 <b>Ссылка:</b> {pay_check['result']['bot_invoice_url'].split("https://")[1]}
⏳ <b>Время на оплату:</b> <code>5 минут</code>

📍 Статус: <code>Время ожидание истекло</code>
""", message.chat.id, msg.id)
            database.reset_pay(message.from_user.id)
            return False
            break
        
        check = cryptopay.getInvoice(coin, pay_check['result']['invoice_id'])
        await sleep(1)
        
    await bot.edit_message_text(f"""
🧾 <b>Чек: </b>
🆔 <b>ID:</b> <code>{pay_check['result']['invoice_id']}</code>
🕹 <b>Игра:</b> <code>{emoji_name}</code>
💵 <b>Сумма:</b> <code>{str(bet)} {coin}</code>
🔗 <b>Ссылка:</b> {pay_check['result']['bot_invoice_url'].split("https://")[1]}
⏳ <b>Время на оплату:</b> <code>5 минут</code>

📍 Статус: <code>Успешная оплата</code>
""", message.chat.id, msg.id)

    print(f"[DEBUG] Succes pay: {pay_check['result']['invoice_id']} owner: {message.from_user.id} | {message.from_user.first_name}")
    
    return True
    

def calc_win(engine: Engine, bet_name: str, emoji_name: str):
    match emoji_name:
        case 'Кости':
            engine.get_win_cube(bet_name)
        case 'Баскетбол':
            engine.get_win_basketball(bet_name)
        case 'Футбол':
            engine.get_win_football(bet_name)
        case 'Дартс':
            engine.get_win_darts(bet_name)
        case 'Слоты':
            engine.get_win_casino(bet_name)

async def handler(message, bet: float, coin: str):
    database = DataBase()
    database.open()
    data = database.find_user_by_id(message.from_user.id)
    database.close()
    
    success_pay = await generate_payment(message, data, bet, coin)
    
    if success_pay == False:
        return
    
    emoji_name = transform_emoji_name_to_textRU(data[UserType.game])
    bet_name = transform_bet(data[UserType.game_bet_to_win])    
    
    await bot.send_message(message.from_user.id, "<i>Оплата успешна! Приятной игры на @MaxBetCasino_tg!</i>", reply_markup=start_keyboard())
    
    
    me = await bot.get_me()
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🕹 Сделать ставку", url=f"https://t.me/{me.username}?start=0"))

#     ✅ Ставка принята в работу!
# ⚡️ От: хуй
# 🎮  Игра: пидр 
# 📤 Исход: хуй
# 💸 Ставка: пизда

#<b><i></i></b>
    
    await bot.send_message(CHANNAL_ID, f"""
<b>✅ Ставка принята в работу!</b>
⚡️ <b>От:</b> <b><i>{(message.from_user.first_name)}</i></b>
🎮 <b>Игра:</b> <b><i>{(emoji_name)}</i></b>
📤 <b>Исход:</b> <b><i>{(transform_bet(data[UserType.game_bet_to_win])[0].upper() + transform_bet(data[UserType.game_bet_to_win])[1:len(transform_bet(data[UserType.game_bet_to_win]))])}</i></b>
💸 <b>Ставка:</b> <b><i>{(bet)} {coin.upper()}</i></b>""", reply_markup=markup)
    
    engine = Engine(bot, message, CHANNAL_ID, transform_text_to_emoji(data[UserType.game]))
    
    if engine.is_duel(bet_name):
        await engine.send_palyer_dice()
        await engine.send_dealer_dice()
    else:
        await engine.send_palyer_dice()

    await sleep(4)
    
    # ЛОЛ ИДИ НАХY
    calc_win(engine, bet_name, emoji_name)
    
    if engine.draw == True:
        await bot.reply_to(engine.player_dice, "<b>Ничья! Переброс!</b> ♻️")
 
        if engine.draw == True:
            while True:
                if engine.draw == False:
                    break
                
                await engine.send_palyer_dice()
                await engine.send_dealer_dice()
                await sleep(4)

                calc_win(engine, bet_name, emoji_name)
                
    
    if engine.draw == True:
        await bot.reply_to(engine.player_dice, "<b>Ничья! Переброс!</b> ♻️")

        while engine.draw == True:
            await engine.send_palyer_dice()
            await engine.send_dealer_dice()
            await sleep(4)

            calc_win(engine, bet_name, emoji_name)

            if engine.draw == False:
                break
            
    if engine.win == True:
        if coin.lower() == "ton":
            money = round(float((bet * TON_USDT) * engine.multi), 3)
        else:
            money = round(float(bet * engine.multi), 3)
        check = cryptopay.createCheck("USDT", str(money), {"pin_to_user_id": message.from_user.id})
        
        if check['ok'] == False:
            if check['error']['name'] == "NOT_ENOUGH_COINS":
                balance = cryptopay.getBalance()
                for admin_id in ADMIN_IDS:
                    await bot.send_message(admin_id, f"""
❗️ <b>Ошибка создать чек для выплаты</b> ❗️
👤 <b>Игрок:</b> <code>{message.from_user.id}</code> {f'<code>{message.from_user.first_name}</code>' if not message.from_user.username else '@' + message.from_user.username}
💰 <b>Сумма вывода:</b> <code>{money}</code>
💸 <b>Доступный баланс</b> <code>{balance["result"][0]["available"]} USDT | {balance["result"][1]["available"]} TON</code>💲
""")
                await bot.reply_to(engine.player_dice, "Ошибка, недостаточно средств на балансе")
                database.open()
                database.reset_pay(message.from_user.id)
                database.close()
                return
            else:
                await bot.reply_to(engine.player_dice, "Ошибка " + check['error']['name'])
                database.open()
                database.reset_pay(message.from_user.id)
                database.close()
                return
            
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🎁 Забрать выигрыш", url=check['result']['bot_check_url']))
        with open("data/assets/victory_image.jpg", "rb") as photo:
            await bot.send_photo(CHANNAL_ID, photo,
                f"""🎉 <b>Поздравляем, вы выиграли! {money}$ ({round(float(money * USDT_RUB), 2)}₽)</b>
<blockquote>Делай ставку ещё раз! Кто знает на чьей стороне будет удача в этот раз!</blockquote>""",
                                 reply_to_message_id=engine.player_dice.id)
        # await bot.reply_to(engine.player_dice,
        #                    f"<b>Победа!</b>\n<blockquote>Поздравляем вы выиграли: {str(money)}! Испытай удачу ещё раз!</blockquote>", reply_markup=markup)
        
        database.open()
        database.reset_pay(message.from_user.id)
        database.execute(f"""UPDATE users SET victories = victories + 1 WHERE user_id = {message.from_user.id}""")
        database.commit()
        database.close()
    else:
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("🕹 Сделать ставку", url=f"https://t.me/{me.username}?start=0"))
        with open("data/assets/lose_image.jpg", "rb") as photo:
            request = requests.get("https://api.forismatic.com/api/1.0/?method=getQuote&format=jsonp&jsonp=?&lang=ru")
            json_data = json.loads(request.text[2:len(request.text) - 1])
            await bot.send_photo(CHANNAL_ID, photo, f"""
<b>К сожалению вы проиграли!</b> 😞
<blockquote>{json_data['quoteText']}</blockquote>
            """)
        # await bot.reply_to(engine.player_dice,
        #                    "<b>Проигрыш!</b>\n<blockquote>Не расстраивайся в следующий раз тебе точно повезет!</blockquote>", reply_markup=markup)
        database.open()
        database.reset_pay(message.from_user.id)
        database.execute(f"""UPDATE users SET losses = losses + 1 WHERE user_id = {message.from_user.id}""")
        database.commit()
        database.close()