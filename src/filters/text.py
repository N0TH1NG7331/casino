from utils.database import DataBase, UserType
from configs import BOT as bot
from engine import register_game

def is_float(string):
    try:
        return isinstance(float(string), float)
    except ValueError:
        return False

async def handler(message):
    database = DataBase()
    database.open()
    data = database.find_user_by_id(message.from_user.id)
    database.close()
    
    if data[UserType.pay_wait_count] == 1:
        split = message.text.split(" ")
        success = False


        try:
            bet = float(split[0])
        except:
            bet = -1
            
        
        if data[UserType.pay_asset] == "TON":
            if bet > 0.0099:
                success = True
        elif data[UserType.pay_asset] == "USDT":
            if bet > 0.099:
                success = True
        
        if success == True:
            await register_game.handler(message, float(bet), data[UserType.pay_asset])
        else:
            await bot.send_message(message.from_user.id, f"❌ <b>Ошибка!</b> <i>Введите сумму ставки от</i> <code>{'0.1' if data[UserType.pay_asset] == 'USDT' else '0.01'}</code> <i>{data[UserType.pay_asset]}</i>")
        
        
        return