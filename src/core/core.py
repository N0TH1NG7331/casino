from callbacks import select_coin
import configs
import os
import json
import sqlite3
import glob
import importlib.util

# from callbacks import profile

def requirements_folders():
    for folder in configs.REQUIREMENTS_FOLDERS:
        if not os.path.exists(folder):
            print("[DEBUG] Creating folder:", folder)
            os.mkdir(folder)

def requirements_files():
    #TODO: Creating users database
    if not os.path.exists("data/users.db"):
        connect = sqlite3.connect("data/users.db")
        cursor = connect.cursor()
        #TODO: DataBase content
        cursor.execute('''
CREATE TABLE "users" (
	"id"	               INTEGER NOT NULL UNIQUE,
    "user_id"              INTEGER NOT NULL,
	"username"	           TEXT,
	"first_name"	       TEXT NOT NULL,
 
	"victories"	           INTEGER,
	"losses"	           INTEGER,
 
	"pay_started"	       INTEGER,
	"pay_id"	           INTEGER,
	"pay_count"	           TEXT,
	"pay_wait_count"	   INTEGER,
    "pay_asset"            TEXT,
 
	"game"	               TEXT,
	"game_bet_to_win"	   TEXT,
 
	"referral_id"	       INTEGER,
	"referral_balance"	   TEXT,
	"invited"	           INTEGER NOT NULL,
	PRIMARY KEY("id")
);
''')

    #TODO: Creating bot statistics
    if not os.path.exists("data/statistics.json"):
        with open("data/statistics.json", "w") as file:
            data = {
                "daily_max_bet.rub": 0,
                
                "payment.per_day": {
                    "usdt": 0,
                    "ton": 0,
                    "rub": 0
                },
                
                "payment.all_time": {
                    "usdt": 0,
                    "ton": 0,
                    "rub": 0
                },
                
                "history.daily_max_bet": {
                    # Example
                    # "date": {
                    #   "bet": 0,
                    #   "winner.id": 0,
                    #   "winner.first_name": ""
                    # }
                }
            }
            
            json.dump(data, file)

async def register_handlers():
    path = "src/handlers"
    files = glob.glob(os.path.join(path, "*.py"))
    
    success = 0
    error = 0
    
    for file_path in files:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, "TRIGGER"):
            TRIGGER = getattr(module, "TRIGGER")
        else:
            print("[ERROR] Not exists var \"TRIGGER\"")
            error += 1
            continue
            
        if hasattr(module, "handler"):
            handler = getattr(module, "handler")
        else:
            print("[ERROR] Not exists functions \"handler\"")
            error += 1
            continue
        success += 1
        configs.BOT.register_message_handler(handler, commands=[TRIGGER])
        
    print(f"[DEBUG] Succes: {success} | Error: {error}")
    
    
# async def register_callbacks():
#     path = "src/callbacks"
#     files = glob.glob(os.path.join(path, "*.py"))
    
#     success = 0
#     error = 0
    
#     for file_path in files:
#         module_name = os.path.splitext(os.path.basename(file_path))[0]
#         print(f"[DEBUG] Trying register handler {module_name}")
        
#         spec = importlib.util.spec_from_file_location(module_name, file_path)
#         module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(module)
        
#         if hasattr(module, "TRIGGER"):
#             TRIGGER = getattr(module, "TRIGGER")
#             print("[DEBUG] Callback trigger:", TRIGGER)
#         else:
#             print("[ERROR] Not exists var \"TRIGGER\"")
#             error += 1
#             continue
            
#         if hasattr(module, "callback"):
#             callback = getattr(module, "callback")
#         else:
#             print("[ERROR] Not exists functions \"callback\"")
#             error += 1
#             continue
        
#         print(f"[DEBUG] Success register {module_name}")
#         success += 1
#         print(f"[DEBUG] Callback: {callback} | Trigger: {TRIGGER}")
#         configs.BOT.register_callback_query_handler(callback, func=lambda call: call.data==TRIGGER)
        
    # print(f"[DEBUG] Succes: {success} | Error: {error}")

async def setup():
    print("[DEBUG] Checkings folders...")
    requirements_folders()
    
    print("[DEBUG] Checkings files...")
    requirements_files()
    
    print("[DEBUG] Register handlers...")
    await register_handlers()
    
    print("[DEBUG] Register callbacks...")
    # await register_callbacks()
    
    from filters import text
    configs.BOT.register_message_handler(text.handler, content_types=["text"])
    
    from callbacks import profile, withdrawel_referral, start, register_bet
    from callbacks import start_game, register_emoji
    
    configs.BOT.register_callback_query_handler(start.callback, func=lambda call: call.data==start.TRIGGER)
    configs.BOT.register_callback_query_handler(profile.callback, func=lambda call: call.data==profile.TRIGGER)
    configs.BOT.register_callback_query_handler(withdrawel_referral.callback, func=lambda call: call.data==withdrawel_referral.TRIGGER)
    
    configs.BOT.register_callback_query_handler(start_game.callback, func=lambda call: call.data==start_game.TRIGGER)
    configs.BOT.register_callback_query_handler(register_emoji.callback_cube, func=lambda call: call.data == "callback__game-cube")
    configs.BOT.register_callback_query_handler(register_emoji.callback_basketball, func=lambda call: call.data == "callback__game-basketball")
    configs.BOT.register_callback_query_handler(register_emoji.callback_football, func=lambda call: call.data == "callback__game-football")
    configs.BOT.register_callback_query_handler(register_emoji.callback_darts, func=lambda call: call.data == "callback__game-darts")
    configs.BOT.register_callback_query_handler(register_emoji.callback_casino, func=lambda call: call.data == "callback__game-casino")
    
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__cube-more")
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__cube-less")
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__cube-even")
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__cube-odd")
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__cube-duel")

    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__bf-hit")
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__bf-miss")
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__bf-duel")

    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__darts-red")
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__darts-white")
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__darts-hit")
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__darts-miss")
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__darts-duel")

    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__casino-blueberries")
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__casino-777")
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__casino-bar")
    configs.BOT.register_callback_query_handler(select_coin.callback, func=lambda call: call.data == "callback__casino-lemons")
    
    configs.BOT.register_callback_query_handler(register_bet.callback, func=lambda call: call.data == "callback__coin-USDT")
    configs.BOT.register_callback_query_handler(register_bet.callback, func=lambda call: call.data == "callback__coin-TON")
    
    
    
    
    
    print("[DEBUG] IDI HAXYI MANUAL SYKA")
    
    print("[DEBUG] Bot success started!")
    await configs.BOT.infinity_polling(10)