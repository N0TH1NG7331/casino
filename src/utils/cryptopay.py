from requests import get, post
class Assets:
    USDT = "USDT"
    TON = "TON"
    GRAM = "GRAM"
    BTC = "BTC"
    ETH = "ETH"
    LTC = "LTC"
    BNB = "BNB"
    TRX = "TRX"
    USDC = "USDC"


class CryptoPay:
    def __init__(self, token: str, testnet: bool=False):
        self.token = str(token)
        self.url = 'https://pay.crypt.bot/api' if testnet == False else 'https://testnet-pay.crypt.bot/api'
        self.headers = {'Content-Type': 'application/json', 'Crypto-Pay-API-Token': self.token}

    def getMe(self, args={}):
        return post(f'{self.url}/getMe', headers=self.headers, json={**args}).json()


    def getBalance(self):
        return post(f'{self.url}/getBalance', headers=self.headers).json()

    def getExchangeRates(self):
        return post(f'{self.url}/getExchangeRates', headers=self.headers).json()

    def getCurrencies(self):
        return post(f'{self.url}/getCurrencies', headers=self.headers).json()

    def getStats(self, args={}):
        return post(f'{self.url}/getStats', headers=self.headers, json={**args}).json()




    #Invoices
    def createInvoice(self, asset: str, amount: str, args={}):
         return post(f'{self.url}/createInvoice', headers=self.headers, json={'asset': asset, 'amount': amount, **args}).json()

    def deleteInvoice(self, invoice_id: int):
        return post(f'{self.url}/deleteInvoice', headers=self.headers, json={'invoice_id': invoice_id}).json()

    def getInvoice(self, asset: str, invoice_id: str, args={}):
        return post(f'{self.url}/getInvoices', headers=self.headers, json={'asset': asset, 'invoice_ids': invoice_id, **args}).json()

    def getInvoices(self, args={}):
        return post(f'{self.url}/getInvoices', headers=self.headers, json={**args}).json()




    #Checks
    def createCheck(self, asset: str, amount: str, args={}):
        return post(f'{self.url}/createCheck', headers=self.headers, json={'asset': asset, 'amount': amount, **args}).json()

    def getCheck(self, asset: str, amount: str, args={}):
        return post(f'{self.url}/getChecks', headers=self.headers, json={'asset': asset, 'amount': amount, **args}).json()

    def getChecks(self, args={}):
        return post(f'{self.url}/getChecks', headers=self.headers, json={**args}).json()




    #Transfer
    def transfer(self, user_id: int, asset: str, amount: str, spend_id: str, args={}):
        return post(f'{self.url}/transfer', headers=self.headers, json={
            'user_id': user_id, 'asset': asset, 'amount': amount, 'spend_id': spend_id, **args}).json()

    def getTransfer(self, asset: str, transfer_id: str, args={}):
        return post(f'{self.url}/getTransfers', headers=self.headers, json={'asset': asset, 'transfer_ids': transfer_id, **args}).json()


    def getTransfers(self, args={}):
        return post(f'{self.url}/getTransfers', headers=self.headers, json={**args}).json()
    
