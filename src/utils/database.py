import sqlite3

class UserType:
    id = 0
    user_id = 1
    username = 2
    first_name = 3
    
    victories = 4
    losses = 5
    
    pay_started = 6
    pay_id = 7
    pay_count = 8
    pay_wait_count = 9
    pay_asset = 10
    
    game = 11
    game_bet_to_win = 12
    
    referral_id = 13
    referral_balance = 14
    invated = 15
    

class DataBase:
    def __ini__(self):
        self.connet = None
        self.cursor = None
        
    def open(self):
        self.connect = sqlite3.connect("data/users.db")
        self.cursor = self.connect.cursor()
        
    def close(self, commit: bool=False):
        if not commit:
            self.connect.close()
            return
        
        self.connect.commit()
        self.connect.close()
        
    def execute(self, command, par=()):
        self.cursor.execute(command, par)
        
    def fexeture(self, command: str):
        if self.connect == None:
            self.connect = sqlite3.connect("data/users.db")
            self.cursor = self.connect.cursor()
        else:
            self.connect.close()
            self.connect = sqlite3.connect("data/users.db")()
        self.cursor.execute(command)
        self.connect.commit()
        self.connect.close()
        
    def commit(self):
        self.connect.commit()
        
    def find_user_by_id(self, id: int) -> dict:
        self.cursor.execute(f'''SELECT * FROM users WHERE user_id = {id}''')
        row = self.cursor.fetchone()
        
        return row
        
    def exists_user(self, id: int) -> int:
        result = self.find_user_by_id(id)
        
        return False if result == None else True
    
    def register_user(self, id: int, username: str, first_name: str, referral_id: int=0):
        if self.exists_user(id):
            return
        
        self.execute(f"""
INSERT INTO users VALUES(
    NULL, {id}, '{username}', '{first_name}',
    0, 0,
    0, 0, NULL, 0, NULL,
    NULL, NULL,
    {referral_id}, 0, 0
)""")
        print(f"[DEBUG] Register new user({id}): {username}")
        self.commit()
        
    def reset_pay(self, id: str):
        if not self.exists_user(id):
            return


        self.execute(f"""UPDATE users SET pay_started = 0 AND pay_id = 0 and pay_count = '' AND pay_wait_count = 0 AND pay_asset = '' AND game = '' AND game_bet_to_win = '' WHERE user_id = {id} """)
        self.commit()