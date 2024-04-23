import telebot

def transform_bet(text):
    v = ""
    match text:
        #Куб
        case "more":
            v = "больше"
        case "less":
            v = "меньше"
        case "even":
            v = "чёт"
        case "odd":
            v = "нечет"
        case "plinko":
            v = "плинко"

        #Баскетбол & Футбол & Дартс
        case "hit":
            v = "гол"
        case "miss":
            v = "промах"

        # Дартс
        case "red":
            v = "красный"
        case "white":
            v = "белый"

        # Слоты
        case "blueberries":
            v = "черника"
        case "777":
            v = "777"
        case "bar":
            v = "бар"
        case "lemons":
            v = "лемоны"

        case "duel":
            v = "дуэль"

    return v

def transform_text_to_emoji(emoji_name):
    v = ""

    match emoji_name:
        case "cube":
            v = "🎲"
        case "basketball":
            v = "🏀"
        case "football":
            v = "⚽️"
        case "darts":
            v = "🎯"
        case "casino":
            v = "🎰"
    return v

def transform_emoji_name_to_textRU(emoji_name):
    v = ""
    match emoji_name:
        case "cube":
            v = "Кости"
        case "basketball":
            v = "Баскетбол"
        case "football":
            v = "Футбол"
        case "darts":
            v = "Дартс"
        case "casino":
            v = "Слоты"
            
    return v

class Engine:
    def __init__(self, bot: telebot.TeleBot, message, channal_id: int, emoji: str):
        self.bot = bot
        self.message = message
        self.channal_id = channal_id
        self.emoji = emoji

        self.multi = 1.0
        self.win = False
        self.draw = False

        self.player_dice = None
        self.player_dice_value = -1

        self.dealer_dice = None
        self.dealer_dice_value = -1

    def is_duel(self, bet_to: str) -> bool:
        return True if bet_to == 'дуэль' else False

    def set_win(self, multi):
        self.win = True
        self.multi = multi

    async def send_palyer_dice(self):
        self.player_dice = await self.bot.send_dice(self.channal_id, self.emoji)
        self.player_dice_value = self.player_dice.dice.value

    async def send_dealer_dice(self):
        self.dealer_dice = await self.bot.send_dice(self.channal_id, self.emoji)
        self.dealer_dice_value = self.dealer_dice.dice.value

    #Ебучая логика на вины
    def get_win_cube(self, bet_to: str):
        match bet_to:
            case 'больше':
                if self.player_dice_value > 3 and self.player_dice_value < 7:
                    self.set_win(1.7)
            case 'меньше':
                if self.player_dice_value > 0 and self.player_dice_value < 4:
                    self.set_win(1.7)
            case 'чёт':
                if not self.player_dice_value % 2:
                    self.set_win(1.7)
            case 'нечет':
                if self.player_dice_value % 2:
                    self.set_win(1.7)
            case 'дуэль':
                #TODO: Fix duel
                if self.player_dice_value > self.dealer_dice_value:
                    self.set_win(1.8)
                    self.draw = False
                elif self.player_dice_value == self.dealer_dice_value or self.dealer_dice_value == self.player_dice_value:
                    self.draw = True
                elif self.dealer_dice_value > self.player_dice_value:
                    self.draw = False
            case 'плинко':
                WINS_VALUE = [
                    [1, False, 0],
                    [2, True, 0.3],
                    [3, True, 0.7],
                    [4, True, 1.2],
                    [5, True, 1.4],
                    [6, True, 1.7]
                ]

                if self.player_dice_value == 1:
                    return


                index_row = self.player_dice_value - 1
                is_win = WINS_VALUE[index_row][1]
                print(self.player_dice_value, WINS_VALUE[index_row][1], WINS_VALUE[index_row][2])
                

                self.set_win(WINS_VALUE[index_row][2])

                # match self.player_dice_value:
                #     case 2:
                #         self.set_win(0.3)

                # for row in WINS_VALUE:
                #     value, win, multi = row[0], row[1], row[2]

                #     if value == self.player_dice_value:
                #         if win == False:
                #             break
                #         self.set_win(multi)

    def get_win_basketball(self, bet_to: str):
        match bet_to:
            case 'гол':
                if self.player_dice_value == 5 or self.player_dice_value == 4:
                    self.set_win(1.6)
            case 'промах':
                if self.player_dice_value > 0 and self.player_dice_value < 4:
                    self.set_win(1.3)

    def get_win_football(self, bet_to: str):
        match bet_to:
            case 'гол':
                if self.player_dice_value > 2 and self.player_dice_value < 6:
                    self.set_win(1.3)
            case 'промах':
                if self.player_dice_value == 1 or self.player_dice_value == 2:
                    self.set_win(1.6)

    def get_win_darts(self, bet_to: str):
        match bet_to:
            case 'красный':
                if self.player_dice_value == 6 or self.player_dice_value == 2 or self.player_dice_value == 4:
                    self.set_win(1.6)
            case 'белый':
                if self.player_dice_value == 5 or self.player_dice_value == 3:
                    self.set_win(1.7)
            case 'гол':
                if self.player_dice_value == 6:
                    self.set_win(2.1)
            case 'промах':
                if self.player_dice_value == 1:
                    self.set_win(1.8)

    def get_win_casino(self, bet_to: str):
        match bet_to:
            case 'лимоны':
                if self.player_dice_value == 43:
                    self.set_win(3.1)
            case 'черника':
                if self.player_dice_value == 22:
                    self.set_win(4.1)
            case '777':
                if self.player_dice_value == 64:
                    self.set_win(13.1)
            case 'бар':
                if self.player_dice_value == 1:
                    self.set_win(5.1)