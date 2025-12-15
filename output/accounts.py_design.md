```python
import datetime

# --- Mock Share Price Function ---
# This is a placeholder for a real-time stock price API.
# In a real application, this would fetch live data.
def get_share_price(symbol: str) -> float:
    """
    Retrieves the current price of a given share symbol.

    Args:
        symbol: The stock symbol (e.g., 'AAPL', 'TSLA', 'GOOGL').

    Returns:
        The current price of the share.
    """
    mock_prices = {
        'AAPL': 170.00,
        'TSLA': 250.00,
        'GOOGL': 1500.00
    }
    return mock_prices.get(symbol, 0.0) # Return 0.0 if symbol not found

# --- Transaction Types ---
class TransactionType:
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    BUY = "BUY"
    SELL = "SELL"

# --- Account Class ---
class Account:
    """
    Represents a user's trading account in the simulation platform.
    Manages funds, share holdings, and transaction history.
    """

    def __init__(self, account_id: str, initial_deposit: float = 0.0):
        """
        Initializes a new trading account.

        Args:
            account_id: A unique identifier for the account.
            initial_deposit: The initial amount of cash deposited into the account.
        """
        if not isinstance(account_id, str) or not account_id:
            raise ValueError("Account ID must be a non-empty string.")
        if not isinstance(initial_deposit, (int, float)) or initial_deposit < 0:
            raise ValueError("Initial deposit must be a non-negative number.")

        self.account_id: str = account_id
        self.balance: float = initial_deposit
        self.initial_deposit: float = initial_deposit # Keep track of the original deposit for P/L calculation
        self.holdings: dict[str, int] = {} # {symbol: quantity}
        self.transactions: list[dict] = [] # List of transaction records

    def _add_transaction(self, transaction_type: str, symbol: str = None, quantity: int = 0, amount: float = 0.0, description: str = ""):
        """
        Internal helper to record a transaction.
        """
        transaction_record = {
            "timestamp": datetime.datetime.now(),
            "type": transaction_type,
            "symbol": symbol,
            "quantity": quantity,
            "amount": amount,
            "balance_after": self.balance,
            "description": description
        }
        self.transactions.append(transaction_record)

    def deposit(self, amount: float):
        """
        Deposits funds into the account.

        Args:
            amount: The amount of money to deposit.

        Raises:
            ValueError: If the deposit amount is not a positive number.
        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Deposit amount must be a positive number.")
        self.balance += amount
        self._add_transaction(TransactionType.DEPOSIT, amount=amount, description=f"Deposit of ${amount:.2f}")
        print(f"Deposit successful. New balance: ${self.balance:.2f}")

    def withdraw(self, amount: float):
        """
        Withdraws funds from the account.

        Args:
            amount: The amount of money to withdraw.

        Raises:
            ValueError: If the withdrawal amount is not a positive number.
            ValueError: If the withdrawal amount exceeds the available balance.
        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Withdrawal amount must be a positive number.")
        if amount > self.balance:
            raise ValueError(f"Insufficient funds. Available balance: ${self.balance:.2f}, requested: ${amount:.2f}")
        self.balance -= amount
        self._add_transaction(TransactionType.WITHDRAWAL, amount=amount, description=f"Withdrawal of ${amount:.2f}")
        print(f"Withdrawal successful. New balance: ${self.balance:.2f}")

    def buy_shares(self, symbol: str, quantity: int):
        """
        Records the purchase of shares.

        Args:
            symbol: The stock symbol (e.g., 'AAPL').
            quantity: The number of shares to buy.

        Raises:
            ValueError: If the symbol is invalid or quantity is not a positive integer.
            ValueError: If the purchase would exceed the available balance.
        """
        if not isinstance(symbol, str) or not symbol:
            raise ValueError("Share symbol must be a non-empty string.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        current_price = get_share_price(symbol)
        if current_price <= 0:
            raise ValueError(f"Invalid or unknown share symbol: {symbol}")

        total_cost = current_price * quantity

        if total_cost > self.balance:
            raise ValueError(f"Insufficient funds to buy {quantity} shares of {symbol}. Cost: ${total_cost:.2f}, Available balance: ${self.balance:.2f}")

        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self._add_transaction(TransactionType.BUY, symbol=symbol, quantity=quantity, amount=total_cost, description=f"Bought {quantity} shares of {symbol} at ${current_price:.2f} each.")
        print(f"Successfully bought {quantity} shares of {symbol} for ${total_cost:.2f}. New balance: ${self.balance:.2f}")

    def sell_shares(self, symbol: str, quantity: int):
        """
        Records the sale of shares.

        Args:
            symbol: The stock symbol (e.g., 'AAPL').
            quantity: The number of shares to sell.

        Raises:
            ValueError: If the symbol is invalid or quantity is not a positive integer.
            ValueError: If the account does not hold enough shares of the given symbol.
        """
        if not isinstance(symbol, str) or not symbol:
            raise ValueError("Share symbol must be a non-empty string.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            current_holdings = self.holdings.get(symbol, 0)
            raise ValueError(f"Insufficient shares to sell. You have {current_holdings} shares of {symbol}, but tried to sell {quantity}.")

        current_price = get_share_price(symbol)
        if current_price <= 0:
            raise ValueError(f"Invalid or unknown share symbol: {symbol}")

        total_revenue = current_price * quantity

        self.balance += total_revenue
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol] # Remove symbol if quantity becomes zero

        self._add_transaction(TransactionType.SELL, symbol=symbol, quantity=quantity, amount=total_revenue, description=f"Sold {quantity} shares of {symbol} at ${current_price:.2f} each.")
        print(f"Successfully sold {quantity} shares of {symbol} for ${total_revenue:.2f}. New balance: ${self.balance:.2f}")

    def get_portfolio_value(self) -> float:
        """
        Calculates the current total value of all held shares.

        Returns:
            The total market value of the portfolio.
        """
        portfolio_value = 0.0
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            portfolio_value += price * quantity
        return portfolio_value

    def get_total_value(self) -> float:
        """
        Calculates the total value of the account, including cash balance and portfolio value.

        Returns:
            The sum of cash balance and portfolio market value.
        """
        return self.balance + self.get_portfolio_value()

    def get_profit_loss(self) -> float:
        """
        Calculates the overall profit or loss from the initial deposit.

        Returns:
            The profit or loss amount. Positive for profit, negative for loss.
        """
        # Profit/Loss is the current total value minus the initial deposit.
        # This is a simplified P/L. A more complex system might track cost basis.
        return self.get_total_value() - self.initial_deposit

    def get_holdings(self) -> dict[str, int]:
        """
        Returns the current holdings of shares.

        Returns:
            A dictionary where keys are share symbols and values are quantities.
        """
        return self.holdings.copy() # Return a copy to prevent external modification

    def get_transactions(self) -> list[dict]:
        """
        Returns the transaction history of the account.

        Returns:
            A list of dictionaries, each representing a transaction.
        """
        return self.transactions.copy() # Return a copy to prevent external modification

    def get_account_summary(self) -> dict:
        """
        Provides a summary of the account's current state.

        Returns:
            A dictionary containing cash balance, portfolio value, total value, and P/L.
        """
        portfolio_value = self.get_portfolio_value()
        total_value = self.balance + portfolio_value
        profit_loss = total_value - self.initial_deposit

        return {
            "account_id": self.account_id,
            "cash_balance": round(self.balance, 2),
            "portfolio_value": round(portfolio_value, 2),
            "total_value": round(total_value, 2),
            "profit_loss": round(profit_loss, 2),
            "initial_deposit": round(self.initial_deposit, 2)
        }

# --- Example Usage (for testing/demonstration) ---
if __name__ == "__main__":
    print("--- Account Management System ---")

    # Create an account
    try:
        my_account = Account("USER123", initial_deposit=10000.0)
        print(f"Account '{my_account.account_id}' created with initial deposit: ${my_account.initial_deposit:.2f}")
        print("Initial Account Summary:", my_account.get_account_summary())
    except ValueError as e:
        print(f"Error creating account: {e}")
        exit()

    print("\n--- Transactions ---")

    # Deposit more funds
    try:
        my_account.deposit(5000.0)
    except ValueError as e:
        print(f"Error depositing funds: {e}")

    # Buy shares
    try:
        my_account.buy_shares("AAPL", 10) # Cost: 10 * 170 = 1700
        print("After buying AAPL:", my_account.get_account_summary())
    except ValueError as e:
        print(f"Error buying shares: {e}")

    try:
        my_account.buy_shares("TSLA", 5) # Cost: 5 * 250 = 1250
        print("After buying TSLA:", my_account.get_account_summary())
    except ValueError as e:
        print(f"Error buying shares: {e}")

    # Attempt to buy more than affordable
    try:
        my_account.buy_shares("GOOGL", 100) # High cost
    except ValueError as e:
        print(f"Attempt to overbuy GOOGL: {e}")
        print("Account Summary after failed GOOGL buy:", my_account.get_account_summary())

    # Sell shares
    try:
        my_account.sell_shares("AAPL", 5) # Revenue: 5 * 170 = 850
        print("After selling AAPL:", my_account.get_account_summary())
    except ValueError as e:
        print(f"Error selling shares: {e}")

    # Attempt to sell more than owned
    try:
        my_account.sell_shares("TSLA", 10) # Own 5, try to sell 10
    except ValueError as e:
        print(f"Attempt to over-sell TSLA: {e}")
        print("Account Summary after failed TSLA sell:", my_account.get_account_summary())

    # Withdraw funds
    try:
        my_account.withdraw(3000.0)
        print("After withdrawing $3000:", my_account.get_account_summary())
    except ValueError as e:
        print(f"Error withdrawing funds: {e}")

    # Attempt to withdraw more than available
    try:
        my_account.withdraw(20000.0) # High withdrawal
    except ValueError as e:
        print(f"Attempt to over-withdraw: {e}")
        print("Account Summary after failed withdrawal:", my_account.get_account_summary())


    print("\n--- Reporting ---")

    # Get holdings
    print("Current Holdings:", my_account.get_holdings())

    # Get account summary
    print("\nFinal Account Summary:")
    print(my_account.get_account_summary())

    # Get transaction history
    print("\nTransaction History:")
    for tx in my_account.get_transactions():
        print(f"- {tx['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} | {tx['type']} | {tx.get('symbol', '')} | Qty: {tx.get('quantity', 0)} | Amt: ${tx.get('amount', 0.0):.2f} | Balance After: ${tx.get('balance_after', 0.0):.2f} | Desc: {tx.get('description', '')}")

    # Demonstrate P/L calculation
    print(f"\nTotal Profit/Loss: ${my_account.get_profit_loss():.2f}")
```