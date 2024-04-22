import json
import datetime as dt
from datetime import datetime

class DailyMaxBet:
    yesterday = (datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
    to_day = str(datetime.now()).split(" ")[0]

class Statistics:
    def __init__(self):
        with open("data/statistics.json") as file:
            self.data = json.load(file)
            
        self.current_data = datetime.now()
        self.current_data_str = str(self.current_data).split(" ")[0]
    
    def dump(self):
        with open("data/statistics.json","w") as file:
            json.dump(file)
    
    def add(self, where: str, what: str, value: any):
        self.data[where][what] = value
        
    def add_history_daily_max_bet(self, where: DailyMaxBet, data):
        self.data['history.daily_max_bet'][where] = data