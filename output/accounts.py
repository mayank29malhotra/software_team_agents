import datetime

class Account:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = initial_balance
        self.profit_loss = 0
    
    def deposit(self, amount):
        self.balance += amount
        self.transactions.append({'type': 'deposit', 'amount': amount, 'timestamp': datetime.datetime.now()})
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError('Insufficient funds')
        self.balance -= amount
        self.transactions.append({'type': 'withdrawal', 'amount': amount, 'timestamp': datetime.datetime.now()})
    
    def buy_shares(self, symbol, quantity):
        price = get_share_price(symbol)
        if price is None:
            raise ValueError('Unknown share symbol')
        cost = price * quantity
        if cost > self.balance:
            raise ValueError('Insufficient funds to buy shares')
        self.balance -= cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transactions.append({'type': 'buy', 'symbol': symbol, 'quantity': quantity, 'price': price, 'timestamp': datetime.datetime.now()})
    
    def sell_shares(self, symbol, quantity):
        if symbol not in self.holdings:
            raise ValueError('You do not own any shares of this symbol')
        if quantity > self.holdings[symbol]:
            raise ValueError('You do not own enough shares to sell')
        price = get_share_price(symbol)
        if price is None:
            raise ValueError('Unknown share symbol')
        revenue = price * quantity
        self.balance += revenue
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transactions.append({'type': 'sell', 'symbol': symbol, 'quantity': quantity, 'price': price, 'timestamp': datetime.datetime.now()})
    
    def get_holdings(self):
        return self.holdings
    
    def get_profit_loss(self):
        return self.balance - self.initial_deposit
    
    def get_transactions(self):
        return self.transactions

def get_share_price(symbol):
    # Test implementation, replace with real-time data API in production
    prices = {'AAPL': 150.0, 'TSLA': 200.0, 'GOOGL': 3000.0}
    return prices.get(symbol)