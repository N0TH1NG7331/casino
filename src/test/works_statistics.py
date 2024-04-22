from utils.statistics import Statistics, DailyMaxBet

v1 = Statistics()
v1.add_history_daily_max_bet(DailyMaxBet.to_day, {
    "bet": 0,
    "winner.id": 0,
    "winner.first_name": ""
})

print(v1.data)