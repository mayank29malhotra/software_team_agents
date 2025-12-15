The user asked for the *content* of `test_accounts.py`. I will provide the complete Python code for this file.

```python
import unittest
import datetime
from unittest.mock import patch

# Assuming accounts.py is in the same directory or accessible in the Python path
# If accounts.py is not directly importable, you might need to adjust sys.path
# For the purpose of this exercise, we assume it is importable.
try:
    from accounts import Account, TransactionType, get_share_price
except ModuleNotFoundError:
    # If accounts.py is not found, this means the environment setup is not correct
    # for running tests alongside the module. For this response, we assume it exists.
    # In a real scenario, you'd ensure accounts.py is in the same directory or PYTHONPATH.
    raise ImportError("Could not import 'accounts' module. Make sure 'accounts.py' is in the same directory or accessible.")


# Mock share prices for testing
# These should align with what get_share_price would return, or what the test expects.
MOCK_PRICES = {
    'AAPL': 170.00,
    'TSLA': 250.00,
    'GOOGL': 1500.00,
    'MSFT': 300.00
}

def mock_get_share_price(symbol: str) -> float:
    """A mock function to simulate get_share_price for testing."""
    return MOCK_PRICES.get(symbol, 0.0) # Return 0.0 if symbol not found in mock data

class TestAccount(unittest.TestCase):

    def setUp(self):
        """Set up a fresh Account instance and mock get_share_price before each test."""
        self.account_id = "TEST_ACC_123"
        self.initial_deposit = 10000.0
        
        # Patch the get_share_price function in the 'accounts' module
        # We use side_effect to provide our mock function
        self.patcher = patch('accounts.get_share_price', side_effect=mock_get_share_price)
        self.mock_get_share_price = self.patcher.start()
        
        # Create a new account instance for each test
        self.account = Account(self.account_id, self.initial_deposit)

    def tearDown(self):
        """Stop the patcher after each test to clean up."""
        self.patcher.stop()

    # --- Initialization Tests ---
    def test_account_initialization_valid(self):
        """Test successful account creation with valid parameters."""
        self.assertEqual(self.account.account_id, self.account_id)
        self.assertEqual(self.account.balance, self.initial_deposit)
        self.assertEqual(self.account.initial_deposit, self.initial_deposit)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])

    def test_account_initialization_invalid_id(self):
        """Test account creation with invalid (empty or non-string) account ID."""
        with self.assertRaisesRegex(ValueError, "Account ID must be a non-empty string."):
            Account("", 1000)
        with self.assertRaisesRegex(ValueError, "Account ID must be a non-empty string."):
            Account(12345, 1000) # Non-string ID
        with self.assertRaisesRegex(ValueError, "Account ID must be a non-empty string."):
            Account(None, 1000) # None ID

    def test_account_initialization_invalid_deposit(self):
        """Test account creation with invalid (negative or non-numeric) initial deposit."""
        with self.assertRaisesRegex(ValueError, "Initial deposit must be a non-negative number."):
            Account("ACC1", -100.0)
        with self.assertRaisesRegex(ValueError, "Initial deposit must be a non-negative number."):
            Account("ACC1", "abc") # Non-numeric deposit
        with self.assertRaisesRegex(ValueError, "Initial deposit must be a non-negative number."):
            Account("ACC1", None) # None deposit

    # --- Deposit Tests ---
    def test_deposit_valid_amount(self):
        """Test successful deposit of a positive amount."""
        deposit_amount = 500.0
        self.account.deposit(deposit_amount)
        self.assertEqual(self.account.balance, self.initial_deposit + deposit_amount)
        self.assertEqual(len(self.account.transactions), 1)
        tx = self.account.transactions[0]
        self.assertEqual(tx['type'], TransactionType.DEPOSIT)
        self.assertEqual(tx['amount'], deposit_amount)
        self.assertEqual(tx['balance_after'], self.initial_deposit + deposit_amount)

    def test_deposit_zero_amount(self):
        """Test deposit of zero amount should raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Deposit amount must be a positive number."):
            self.account.deposit(0.0)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change

    def test_deposit_negative_amount(self):
        """Test deposit of negative amount should raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Deposit amount must be a positive number."):
            self.account.deposit(-100.0)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change

    def test_deposit_non_numeric_amount(self):
        """Test deposit of non-numeric amount should raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Deposit amount must be a positive number."):
            self.account.deposit("invalid")
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change

    # --- Withdrawal Tests ---
    def test_withdraw_valid_amount(self):
        """Test successful withdrawal of a positive amount."""
        withdraw_amount = 500.0
        self.account.withdraw(withdraw_amount)
        self.assertEqual(self.account.balance, self.initial_deposit - withdraw_amount)
        self.assertEqual(len(self.account.transactions), 1)
        tx = self.account.transactions[0]
        self.assertEqual(tx['type'], TransactionType.WITHDRAWAL)
        self.assertEqual(tx['amount'], withdraw_amount)
        self.assertEqual(tx['balance_after'], self.initial_deposit - withdraw_amount)

    def test_withdraw_insufficient_funds(self):
        """Test withdrawal exceeding available balance."""
        withdraw_amount = self.initial_deposit + 100.0
        with self.assertRaisesRegex(ValueError, "Insufficient funds. Available balance: .* requested: .*"):
            self.account.withdraw(withdraw_amount)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should remain unchanged

    def test_withdraw_zero_amount(self):
        """Test withdrawal of zero amount should raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Withdrawal amount must be a positive number."):
            self.account.withdraw(0.0)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change

    def test_withdraw_negative_amount(self):
        """Test withdrawal of negative amount should raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Withdrawal amount must be a positive number."):
            self.account.withdraw(-100.0)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change

    def test_withdraw_non_numeric_amount(self):
        """Test withdrawal of non-numeric amount should raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Withdrawal amount must be a positive number."):
            self.account.withdraw("invalid")
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change

    # --- Buy Shares Tests ---
    def test_buy_shares_valid(self):
        """Test successful purchase of shares."""
        symbol = 'AAPL'
        quantity = 10
        price = MOCK_PRICES[symbol]
        cost = quantity * price

        self.account.buy_shares(symbol, quantity)

        self.assertEqual(self.account.balance, self.initial_deposit - cost)
        self.assertEqual(self.account.holdings.get(symbol), quantity)
        self.assertEqual(len(self.account.transactions), 1)
        tx = self.account.transactions[0]
        self.assertEqual(tx['type'], TransactionType.BUY)
        self.assertEqual(tx['symbol'], symbol)
        self.assertEqual(tx['quantity'], quantity)
        self.assertEqual(tx['amount'], cost) # Amount here represents the total cost
        self.assertAlmostEqual(tx['balance_after'], self.initial_deposit - cost, places=2)

    def test_buy_shares_insufficient_funds(self):
        """Test attempting to buy shares when funds are insufficient."""
        symbol = 'AAPL'
        quantity = 100 # Cost: 100 * 170 = 17000, which is > 10000
        with self.assertRaisesRegex(ValueError, "Insufficient funds to buy .* Cost: .* Available balance: .*"):
            self.account.buy_shares(symbol, quantity)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change
        self.assertNotIn(symbol, self.account.holdings) # Holdings should not change

    def test_buy_shares_invalid_symbol(self):
        """Test buying shares with an unknown/invalid symbol."""
        symbol = 'INVALID_STOCK'
        quantity = 10
        with self.assertRaisesRegex(ValueError, f"Invalid or unknown share symbol: {symbol}"):
            self.account.buy_shares(symbol, quantity)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change
        self.assertNotIn(symbol, self.account.holdings) # Holdings should not change

    def test_buy_shares_invalid_quantity_zero(self):
        """Test buying shares with zero quantity."""
        symbol = 'AAPL'
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.buy_shares(symbol, 0)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_buy_shares_invalid_quantity_negative(self):
        """Test buying shares with negative quantity."""
        symbol = 'AAPL'
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.buy_shares(symbol, -5)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_buy_shares_invalid_quantity_float(self):
        """Test buying shares with non-integer quantity."""
        symbol = 'AAPL'
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.buy_shares(symbol, 10.5)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_buy_shares_invalid_symbol_type(self):
        """Test buying shares with non-string symbol type."""
        symbol = 12345 # Invalid type
        quantity = 10
        with self.assertRaisesRegex(ValueError, "Share symbol must be a non-empty string."):
            self.account.buy_shares(symbol, quantity)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_buy_shares_empty_symbol(self):
        """Test buying shares with empty string symbol."""
        symbol = ""
        quantity = 10
        with self.assertRaisesRegex(ValueError, "Share symbol must be a non-empty string."):
            self.account.buy_shares(symbol, quantity)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_buy_shares_multiple_same_symbol(self):
        """Test buying shares of the same symbol multiple times."""
        symbol = 'GOOGL'
        quantity1 = 2
        quantity2 = 3
        price = MOCK_PRICES[symbol]
        cost1 = quantity1 * price
        cost2 = quantity2 * price

        self.account.buy_shares(symbol, quantity1)
        self.account.buy_shares(symbol, quantity2)

        self.assertEqual(self.account.balance, self.initial_deposit - cost1 - cost2)
        self.assertEqual(self.account.holdings.get(symbol), quantity1 + quantity2)
        self.assertEqual(len(self.account.transactions), 2)

    # --- Sell Shares Tests ---
    def test_sell_shares_valid(self):
        """Test successful sale of shares."""
        # First, buy some shares to own them
        symbol = 'TSLA'
        buy_quantity = 5
        buy_price = MOCK_PRICES[symbol]
        buy_cost = buy_quantity * buy_price
        self.account.buy_shares(symbol, buy_quantity)

        # Now, sell a portion of them
        sell_quantity = 2
        sell_price = MOCK_PRICES[symbol] # Use mock price for sale
        sell_revenue = sell_quantity * sell_price

        self.account.sell_shares(symbol, sell_quantity)

        self.assertEqual(self.account.balance, self.initial_deposit - buy_cost + sell_revenue)
        self.assertEqual(self.account.holdings.get(symbol), buy_quantity - sell_quantity)
        self.assertEqual(len(self.account.transactions), 2) # One buy, one sell
        tx = self.account.transactions[-1] # Get the last transaction (the sell)
        self.assertEqual(tx['type'], TransactionType.SELL)
        self.assertEqual(tx['symbol'], symbol)
        self.assertEqual(tx['quantity'], sell_quantity)
        self.assertEqual(tx['amount'], sell_revenue) # Amount here represents the total revenue
        self.assertAlmostEqual(tx['balance_after'], self.initial_deposit - buy_cost + sell_revenue, places=2)

    def test_sell_shares_insufficient_holdings(self):
        """Test attempting to sell more shares than currently owned."""
        symbol = 'AAPL'
        buy_quantity = 5
        self.account.buy_shares(symbol, buy_quantity)

        sell_quantity = 10 # Trying to sell more than owned
        with self.assertRaisesRegex(ValueError, "Insufficient shares to sell. You have .* shares of .* but tried to sell .*"):
            self.account.sell_shares(symbol, sell_quantity)
        self.assertEqual(self.account.holdings.get(symbol), buy_quantity) # Holdings should remain unchanged
        self.assertEqual(self.account.balance, self.initial_deposit - (buy_quantity * MOCK_PRICES[symbol])) # Balance should remain unchanged

    def test_sell_shares_invalid_symbol(self):
        """Test selling shares of a symbol not held by the account."""
        symbol = 'MSFT' # Not bought
        quantity = 5
        with self.assertRaisesRegex(ValueError, "Insufficient shares to sell."): # Message is generic if symbol not in holdings
            self.account.sell_shares(symbol, quantity)
        self.assertNotIn(symbol, self.account.holdings) # Should not be in holdings

    def test_sell_shares_invalid_quantity_zero(self):
        """Test selling shares with zero quantity."""
        symbol = 'AAPL'
        self.account.buy_shares(symbol, 10) # Buy some first
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.sell_shares(symbol, 0)
        self.assertEqual(self.account.holdings.get(symbol), 10) # Holdings unchanged

    def test_sell_shares_invalid_quantity_negative(self):
        """Test selling shares with negative quantity."""
        symbol = 'AAPL'
        self.account.buy_shares(symbol, 10)
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.sell_shares(symbol, -5)
        self.assertEqual(self.account.holdings.get(symbol), 10) # Holdings unchanged

    def test_sell_shares_invalid_quantity_float(self):
        """Test selling shares with non-integer quantity."""
        symbol = 'AAPL'
        self.account.buy_shares(symbol, 10)
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.sell_shares(symbol, 5.5)
        self.assertEqual(self.account.holdings.get(symbol), 10) # Holdings unchanged

    def test_sell_shares_invalid_symbol_type(self):
        """Test selling shares with non-string symbol type."""
        symbol = 54321 # Invalid type
        quantity = 10
        with self.assertRaisesRegex(ValueError, "Share symbol must be a non-empty string."):
            self.account.sell_shares(symbol, quantity)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_sell_shares_empty_symbol(self):
        """Test selling shares with empty string symbol."""
        symbol = ""
        quantity = 10
        with self.assertRaisesRegex(ValueError, "Share symbol must be a non-empty string."):
            self.account.sell_shares(symbol, quantity)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_sell_all_shares_of_symbol(self):
        """Test selling all owned shares of a specific symbol."""
        symbol = 'GOOGL'
        quantity = 3
        self.account.buy_shares(symbol, quantity)
        
        initial_balance_after_buy = self.account.balance
        sell_revenue = quantity * MOCK_PRICES[symbol]

        self.account.sell_shares(symbol, quantity)

        self.assertEqual(self.account.balance, initial_balance_after_buy + sell_revenue)
        self.assertNotIn(symbol, self.account.holdings) # Should be removed from holdings
        self.assertEqual(len(self.account.transactions), 2) # One buy, one sell

    # --- Portfolio Value Tests ---
    def test_get_portfolio_value_empty(self):
        """Test portfolio value when the account has no holdings."""
        self.assertEqual(self.account.get_portfolio_value(), 0.0)

    def test_get_portfolio_value_with_holdings(self):
        """Test portfolio value calculation with multiple holdings."""
        self.account.buy_shares('AAPL', 10) # 10 * 170 = 1700
        self.account.buy_shares('TSLA', 5)  # 5 * 250 = 1250
        
        expected_value = (10 * MOCK_PRICES['AAPL']) + (5 * MOCK_PRICES['TSLA'])
        self.assertAlmostEqual(self.account.get_portfolio_value(), expected_value, places=2)

    def test_get_portfolio_value_after_sell(self):
        """Test portfolio value after selling some shares."""
        self.account.buy_shares('AAPL', 10) # 1700
        self.account.buy_shares('TSLA', 5)  # 1250
        self.account.sell_shares('AAPL', 5) # Sell 5 AAPL, revenue: 5 * 170 = 850

        # Remaining holdings: 5 AAPL, 5 TSLA
        expected_value = (5 * MOCK_PRICES['AAPL']) + (5 * MOCK_PRICES['TSLA'])
        self.assertAlmostEqual(self.account.get_portfolio_value(), expected_value, places=2)

    # --- Total Value Tests ---
    def test_get_total_value_initial(self):
        """Test total value with only initial cash balance."""
        self.assertAlmostEqual(self.account.get_total_value(), self.initial_deposit, places=2)

    def test_get_total_value_with_holdings(self):
        """Test total value calculation including cash and portfolio."""
        self.account.buy_shares('AAPL', 10) # Cost: 1700
        # Balance = 10000 - 1700 = 8300
        # Holdings: AAPL: 10, Value: 10 * 170 = 1700
        # Total Value = Balance + Portfolio Value = 8300 + 1700 = 10000
        self.assertAlmostEqual(self.account.get_total_value(), self.initial_deposit, places=2)

    def test_get_total_value_after_sell_and_deposit(self):
        """Test total value after sell and deposit."""
        self.account.buy_shares('AAPL', 10) # Cost: 1700
        self.account.sell_shares('AAPL', 5) # Revenue: 850
        self.account.deposit(1000)

        # Initial Deposit: 10000
        # After buy: Balance = 10000 - 1700 = 8300, Holdings: AAPL: 10
        # After sell: Balance = 8300 + 850 = 9150, Holdings: AAPL: 5
        # After deposit: Balance = 9150 + 1000 = 10150, Holdings: AAPL: 5
        
        # Current state: Balance = 10150
        # Holdings: AAPL: 5, Portfolio Value = 5 * 170 = 850
        # Total Value = Balance + Portfolio Value = 10150 + 850 = 11000

        expected_total_value = 11000.0
        self.assertAlmostEqual(self.account.get_total_value(), expected_total_value, places=2)

    # --- Profit/Loss Tests ---
    def test_get_profit_loss_initial_state(self):
        """Test P/L calculation when only initial deposit exists (should be 0)."""
        self.assertAlmostEqual(self.account.get_profit_loss(), 0.0, places=2)

    def test_get_profit_loss_after_buy_same_price(self):
        """Test P/L after buying shares at the same price as mock price (should be 0)."""
        symbol = 'AAPL'
        quantity = 10
        self.account.buy_shares(symbol, quantity)
        # Since buy price == mock price and no sell occurs, P/L should still be 0
        # as total_value == initial_deposit
        self.assertAlmostEqual(self.account.get_profit_loss(), 0.0, places=2)

    def test_get_profit_loss_after_sell_at_profit(self):
        """Test P/L after selling shares at a profit (simulated price increase)."""
        symbol = 'GOOGL'
        quantity = 2
        buy_cost = quantity * MOCK_PRICES[symbol]
        self.account.buy_shares(symbol, quantity) # Balance: 10000 - 3000 = 7000

        # Simulate a price increase for selling
        def mock_price_increase(sym):
            if sym == 'GOOGL':
                return MOCK_PRICES[sym] * 1.1 # 10% increase
            return MOCK_PRICES.get(sym, 0.0)
        
        self.mock_get_share_price.side_effect = mock_price_increase
        
        sell_revenue = quantity * mock_price_increase(symbol) # 2 * 1650 = 3300
        self.account.sell_shares(symbol, quantity) # Balance: 7000 + 3300 = 10300

        # Total Value = 10300 (cash) + 0 (holdings gone) = 10300
        # P/L = Total Value - Initial Deposit = 10300 - 10000 = 300
        expected_pl = sell_revenue - buy_cost # This is the actual profit realized
        self.assertAlmostEqual(self.account.get_profit_loss(), expected_pl, places=2)

    def test_get_profit_loss_after_sell_at_loss(self):
        """Test P/L after selling shares at a loss (simulated price decrease)."""
        symbol = 'MSFT'
        quantity = 10
        buy_cost = quantity * MOCK_PRICES[symbol] # 10 * 300 = 3000
        self.account.buy_shares(symbol, quantity) # Balance: 10000 - 3000 = 7000

        # Simulate a price decrease for selling
        def mock_price_decrease(sym):
            if sym == 'MSFT':
                return MOCK_PRICES[sym] * 0.9 # 10% decrease
            return MOCK_PRICES.get(sym, 0.0)
        
        self.mock_get_share_price.side_effect = mock_price_decrease
        
        sell_revenue = quantity * mock_price_decrease(symbol) # 10 * 270 = 2700
        self.account.sell_shares(symbol, quantity) # Balance: 7000 + 2700 = 9700

        # Total Value = 9700 (cash) + 0 (holdings gone) = 9700
        # P/L = Total Value - Initial Deposit = 9700 - 10000 = -300
        expected_pl = sell_revenue - buy_cost # This is the actual loss realized
        self.assertAlmostEqual(self.account.get_profit_loss(), expected_pl, places=2)

    def test_get_profit_loss_with_unrealized_gain(self):
        """Test P/L with unrealized gain (holdings value > cost basis)."""
        buy_symbol = 'AAPL'
        buy_quantity = 5
        buy_cost = buy_quantity * MOCK_PRICES[buy_symbol] # 5 * 170 = 850
        self.account.buy_shares(buy_symbol, buy_quantity) # Balance: 10000 - 850 = 9150

        # Simulate a price increase for holdings valuation
        def mock_price_increase(sym):
            if sym == 'AAPL':
                return MOCK_PRICES[sym] * 1.2 # 20% increase
            return MOCK_PRICES.get(sym, 0.0)
        
        self.mock_get_share_price.side_effect = mock_price_increase
        
        # Current holdings value: 5 * (170 * 1.2) = 5 * 204 = 1020
        # Current cash balance: 9150
        # Total Value = 9150 + 1020 = 10170
        # P/L = 10170 - 10000 = 170
        expected_pl = (10170.0) - self.initial_deposit
        self.assertAlmostEqual(self.account.get_profit_loss(), expected_pl, places=2)

    # --- Get Holdings Tests ---
    def test_get_holdings_empty_account(self):
        """Test get_holdings on an account with no shares."""
        self.assertEqual(self.account.get_holdings(), {})

    def test_get_holdings_after_buys(self):
        """Test get_holdings after buying multiple stocks."""
        self.account.buy_shares('AAPL', 10)
        self.account.buy_shares('TSLA', 5)
        expected = {'AAPL': 10, 'TSLA': 5}
        self.assertEqual(self.account.get_holdings(), expected)

    def test_get_holdings_after_sell(self):
        """Test get_holdings after selling some shares."""
        self.account.buy_shares('AAPL', 10)
        self.account.buy_shares('TSLA', 5)
        self.account.sell_shares('AAPL', 3)
        expected = {'AAPL': 7, 'TSLA': 5}
        self.assertEqual(self.account.get_holdings(), expected)

    def test_get_holdings_after_selling_all(self):
        """Test get_holdings after selling all shares of a stock."""
        self.account.buy_shares('AAPL', 10)
        self.account.sell_shares('AAPL', 10)
        self.assertNotIn('AAPL', self.account.holdings)
        self.assertEqual(self.account.get_holdings(), {})

    def test_get_holdings_returns_copy(self):
        """Test that get_holdings returns a copy, not the original dictionary."""
        self.account.buy_shares('AAPL', 10)
        holdings_copy = self.account.get_holdings()
        holdings_copy['AAPL'] = 100 # Modify the copy
        # Original holdings should remain unchanged
        self.assertEqual(self.account.holdings.get('AAPL'), 10)
        self.assertNotEqual(holdings_copy.get('AAPL'), self.account.holdings.get('AAPL'))

    # --- Get Transactions Tests ---
    def test_get_transactions_empty(self):
        """Test get_transactions on an account with no transactions."""
        self.assertEqual(self.account.get_transactions(), [])

    def test_get_transactions_after_operations(self):
        """Test get_transactions after various account operations."""
        self.account.deposit(1000)
        self.account.buy_shares('AAPL', 5)
        self.account.sell_shares('AAPL', 2)
        self.account.withdraw(500)

        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 4)
        
        # Check types and order
        self.assertEqual(transactions[0]['type'], TransactionType.DEPOSIT)
        self.assertEqual(transactions[1]['type'], TransactionType.BUY)
        self.assertEqual(transactions[2]['type'], TransactionType.SELL)
        self.assertEqual(transactions[3]['type'], TransactionType.WITHDRAWAL)
        
        # Check details of one transaction (e.g., the last one)
        self.assertEqual(transactions[3]['amount'], 500)
        self.assertIn('timestamp', transactions[3])

    def test_get_transactions_returns_copy(self):
        """Test that get_transactions returns a copy, not the original list."""
        self.account.deposit(100)
        transactions_list = self.account.get_transactions()
        transactions_list.append({"dummy_tx": True}) # Modify the returned list
        # Original transactions list should remain unchanged
        self.assertEqual(len(self.account.transactions), 1)
        self.assertNotEqual(len(transactions_list), len(self.account.transactions))

    # --- Get Account Summary Tests ---
    def test_get_account_summary_initial_state(self):
        """Test the account summary for a newly created account."""
        summary = self.account.get_account_summary()
        self.assertEqual(summary['account_id'], self.account_id)
        self.assertAlmostEqual(summary['cash_balance'], self.initial_deposit, places=2)
        self.assertAlmostEqual(summary['portfolio_value'], 0.0, places=2)
        self.assertAlmostEqual(summary['total_value'], self.initial_deposit, places=2)
        self.assertAlmostEqual(summary['profit_loss'], 0.0, places=2)
        self.assertAlmostEqual(summary['initial_deposit'], self.initial_deposit, places=2)

    def test_get_account_summary_after_trades(self):
        """Test the account summary after performing buy and sell operations."""
        self.account.buy_shares('AAPL', 10) # Cost: 1700. Balance: 8300. Portfolio: 1700.
        self.account.buy_shares('TSLA', 2)  # Cost: 500. Balance: 7800. Portfolio: 1700 + 500 = 2200.
        self.account.sell_shares('AAPL', 5) # Revenue: 850. Balance: 7800 + 850 = 8650. Portfolio: (5*170) + (2*250) = 850 + 500 = 1350.

        summary = self.account.get_account_summary()
        
        # Expected values after trades:
        # Cash balance: 10000 - 1700 + 850 = 9150 (This is wrong, used initial deposit - cost + revenue)
        # Let's recalculate based on account operations:
        # Initial: 10000
        # Buy 10 AAPL: 10000 - (10*170) = 10000 - 1700 = 8300
        # Buy 2 TSLA: 8300 - (2*250) = 8300 - 500 = 7800
        # Sell 5 AAPL: 7800 + (5*170) = 7800 + 850 = 8650
        expected_cash_balance = 8650.0
        
        # Holdings: 5 AAPL, 2 TSLA
        # Portfolio Value: (5 * 170) + (2 * 250) = 850 + 500 = 1350.0
        expected_portfolio_value = 1350.0

        # Total Value = Cash Balance + Portfolio Value = 8650.0 + 1350.0 = 10000.0
        expected_total_value = expected_cash_balance + expected_portfolio_value
        
        # Profit/Loss = Total Value - Initial Deposit = 10000.0 - 10000.0 = 0.0
        expected_pl = expected_total_value - self.initial_deposit

        self.assertAlmostEqual(summary['cash_balance'], expected_cash_balance, places=2)
        self.assertAlmostEqual(summary['portfolio_value'], expected_portfolio_value, places=2)
        self.assertAlmostEqual(summary['total_value'], expected_total_value, places=2)
        self.assertAlmostEqual(summary['profit_loss'], expected_pl, places=2)
        self.assertAlmostEqual(summary['initial_deposit'], self.initial_deposit, places=2)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
```
This code defines a `TestAccount` class that inherits from `unittest.TestCase`.
- `setUp` method: Initializes a new `Account` object and mocks the `get_share_price` function before each test method runs. This ensures tests are isolated.
- `tearDown` method: Stops the mock after each test.
- Various test methods (`test_...`): Each method tests a specific piece of functionality of the `Account` class, covering:
    - Initialization (valid and invalid cases).
    - Deposits (valid, zero, negative, non-numeric).
    - Withdrawals (valid, insufficient funds, zero, negative, non-numeric).
    - Buying shares (valid, insufficient funds, invalid symbol, invalid quantity, invalid symbol type).
    - Selling shares (valid, insufficient holdings, invalid symbol, invalid quantity, invalid symbol type).
    - Portfolio value calculation.
    - Total account value calculation.
    - Profit/Loss calculation (including unrealized gains/losses).
    - Retrieving holdings.
    - Retrieving transaction history.
    - Getting account summary.
- `MOCK_PRICES` dictionary and `mock_get_share_price` function are used to control the `get_share_price` behavior during tests.
- `unittest.main()` is called to run the tests when the script is executed directly.

This `test_accounts.py` file can be saved in the same directory as `accounts.py` and run using a test runner like `python -m unittest test_accounts.py`.```python
import unittest
import datetime
from unittest.mock import patch

# Assuming accounts.py is in the same directory or accessible in the Python path
# If accounts.py is not directly importable, you might need to adjust sys.path
# For the purpose of this exercise, we assume it is importable.
try:
    from accounts import Account, TransactionType, get_share_price
except ModuleNotFoundError:
    # If accounts.py is not found, this means the environment setup is not correct
    # for running tests alongside the module. For this response, we assume it exists.
    # In a real scenario, you'd ensure accounts.py is in the same directory or PYTHONPATH.
    raise ImportError("Could not import 'accounts' module. Make sure 'accounts.py' is in the same directory or accessible.")


# Mock share prices for testing
# These should align with what get_share_price would return, or what the test expects.
MOCK_PRICES = {
    'AAPL': 170.00,
    'TSLA': 250.00,
    'GOOGL': 1500.00,
    'MSFT': 300.00
}

def mock_get_share_price(symbol: str) -> float:
    """A mock function to simulate get_share_price for testing."""
    return MOCK_PRICES.get(symbol, 0.0) # Return 0.0 if symbol not found in mock data

class TestAccount(unittest.TestCase):

    def setUp(self):
        """Set up a fresh Account instance and mock get_share_price before each test."""
        self.account_id = "TEST_ACC_123"
        self.initial_deposit = 10000.0
        
        # Patch the get_share_price function in the 'accounts' module
        # We use side_effect to provide our mock function
        self.patcher = patch('accounts.get_share_price', side_effect=mock_get_share_price)
        self.mock_get_share_price = self.patcher.start()
        
        # Create a new account instance for each test
        self.account = Account(self.account_id, self.initial_deposit)

    def tearDown(self):
        """Stop the patcher after each test to clean up."""
        self.patcher.stop()

    # --- Initialization Tests ---
    def test_account_initialization_valid(self):
        """Test successful account creation with valid parameters."""
        self.assertEqual(self.account.account_id, self.account_id)
        self.assertEqual(self.account.balance, self.initial_deposit)
        self.assertEqual(self.account.initial_deposit, self.initial_deposit)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])

    def test_account_initialization_invalid_id(self):
        """Test account creation with invalid (empty or non-string) account ID."""
        with self.assertRaisesRegex(ValueError, "Account ID must be a non-empty string."):
            Account("", 1000)
        with self.assertRaisesRegex(ValueError, "Account ID must be a non-empty string."):
            Account(12345, 1000) # Non-string ID
        with self.assertRaisesRegex(ValueError, "Account ID must be a non-empty string."):
            Account(None, 1000) # None ID

    def test_account_initialization_invalid_deposit(self):
        """Test account creation with invalid (negative or non-numeric) initial deposit."""
        with self.assertRaisesRegex(ValueError, "Initial deposit must be a non-negative number."):
            Account("ACC1", -100.0)
        with self.assertRaisesRegex(ValueError, "Initial deposit must be a non-negative number."):
            Account("ACC1", "abc") # Non-numeric deposit
        with self.assertRaisesRegex(ValueError, "Initial deposit must be a non-negative number."):
            Account("ACC1", None) # None deposit

    # --- Deposit Tests ---
    def test_deposit_valid_amount(self):
        """Test successful deposit of a positive amount."""
        deposit_amount = 500.0
        self.account.deposit(deposit_amount)
        self.assertEqual(self.account.balance, self.initial_deposit + deposit_amount)
        self.assertEqual(len(self.account.transactions), 1)
        tx = self.account.transactions[0]
        self.assertEqual(tx['type'], TransactionType.DEPOSIT)
        self.assertEqual(tx['amount'], deposit_amount)
        self.assertEqual(tx['balance_after'], self.initial_deposit + deposit_amount)

    def test_deposit_zero_amount(self):
        """Test deposit of zero amount should raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Deposit amount must be a positive number."):
            self.account.deposit(0.0)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change

    def test_deposit_negative_amount(self):
        """Test deposit of negative amount should raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Deposit amount must be a positive number."):
            self.account.deposit(-100.0)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change

    def test_deposit_non_numeric_amount(self):
        """Test deposit of non-numeric amount should raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Deposit amount must be a positive number."):
            self.account.deposit("invalid")
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change

    # --- Withdrawal Tests ---
    def test_withdraw_valid_amount(self):
        """Test successful withdrawal of a positive amount."""
        withdraw_amount = 500.0
        self.account.withdraw(withdraw_amount)
        self.assertEqual(self.account.balance, self.initial_deposit - withdraw_amount)
        self.assertEqual(len(self.account.transactions), 1)
        tx = self.account.transactions[0]
        self.assertEqual(tx['type'], TransactionType.WITHDRAWAL)
        self.assertEqual(tx['amount'], withdraw_amount)
        self.assertEqual(tx['balance_after'], self.initial_deposit - withdraw_amount)

    def test_withdraw_insufficient_funds(self):
        """Test withdrawal exceeding available balance."""
        withdraw_amount = self.initial_deposit + 100.0
        with self.assertRaisesRegex(ValueError, "Insufficient funds. Available balance: .* requested: .*"):
            self.account.withdraw(withdraw_amount)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should remain unchanged

    def test_withdraw_zero_amount(self):
        """Test withdrawal of zero amount should raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Withdrawal amount must be a positive number."):
            self.account.withdraw(0.0)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change

    def test_withdraw_negative_amount(self):
        """Test withdrawal of negative amount should raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Withdrawal amount must be a positive number."):
            self.account.withdraw(-100.0)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change

    def test_withdraw_non_numeric_amount(self):
        """Test withdrawal of non-numeric amount should raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Withdrawal amount must be a positive number."):
            self.account.withdraw("invalid")
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change

    # --- Buy Shares Tests ---
    def test_buy_shares_valid(self):
        """Test successful purchase of shares."""
        symbol = 'AAPL'
        quantity = 10
        price = MOCK_PRICES[symbol]
        cost = quantity * price

        self.account.buy_shares(symbol, quantity)

        self.assertEqual(self.account.balance, self.initial_deposit - cost)
        self.assertEqual(self.account.holdings.get(symbol), quantity)
        self.assertEqual(len(self.account.transactions), 1)
        tx = self.account.transactions[0]
        self.assertEqual(tx['type'], TransactionType.BUY)
        self.assertEqual(tx['symbol'], symbol)
        self.assertEqual(tx['quantity'], quantity)
        self.assertEqual(tx['amount'], cost) # Amount here represents the total cost
        self.assertAlmostEqual(tx['balance_after'], self.initial_deposit - cost, places=2)

    def test_buy_shares_insufficient_funds(self):
        """Test attempting to buy shares when funds are insufficient."""
        symbol = 'AAPL'
        quantity = 100 # Cost: 100 * 170 = 17000, which is > 10000
        with self.assertRaisesRegex(ValueError, "Insufficient funds to buy .* Cost: .* Available balance: .*"):
            self.account.buy_shares(symbol, quantity)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change
        self.assertNotIn(symbol, self.account.holdings) # Holdings should not change

    def test_buy_shares_invalid_symbol(self):
        """Test buying shares with an unknown/invalid symbol."""
        symbol = 'INVALID_STOCK'
        quantity = 10
        with self.assertRaisesRegex(ValueError, f"Invalid or unknown share symbol: {symbol}"):
            self.account.buy_shares(symbol, quantity)
        self.assertEqual(self.account.balance, self.initial_deposit) # Balance should not change
        self.assertNotIn(symbol, self.account.holdings) # Holdings should not change

    def test_buy_shares_invalid_quantity_zero(self):
        """Test buying shares with zero quantity."""
        symbol = 'AAPL'
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.buy_shares(symbol, 0)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_buy_shares_invalid_quantity_negative(self):
        """Test buying shares with negative quantity."""
        symbol = 'AAPL'
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.buy_shares(symbol, -5)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_buy_shares_invalid_quantity_float(self):
        """Test buying shares with non-integer quantity."""
        symbol = 'AAPL'
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.buy_shares(symbol, 10.5)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_buy_shares_invalid_symbol_type(self):
        """Test buying shares with non-string symbol type."""
        symbol = 12345 # Invalid type
        quantity = 10
        with self.assertRaisesRegex(ValueError, "Share symbol must be a non-empty string."):
            self.account.buy_shares(symbol, quantity)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_buy_shares_empty_symbol(self):
        """Test buying shares with empty string symbol."""
        symbol = ""
        quantity = 10
        with self.assertRaisesRegex(ValueError, "Share symbol must be a non-empty string."):
            self.account.buy_shares(symbol, quantity)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_buy_shares_multiple_same_symbol(self):
        """Test buying shares of the same symbol multiple times."""
        symbol = 'GOOGL'
        quantity1 = 2
        quantity2 = 3
        price = MOCK_PRICES[symbol]
        cost1 = quantity1 * price
        cost2 = quantity2 * price

        self.account.buy_shares(symbol, quantity1)
        self.account.buy_shares(symbol, quantity2)

        self.assertEqual(self.account.balance, self.initial_deposit - cost1 - cost2)
        self.assertEqual(self.account.holdings.get(symbol), quantity1 + quantity2)
        self.assertEqual(len(self.account.transactions), 2)

    # --- Sell Shares Tests ---
    def test_sell_shares_valid(self):
        """Test successful sale of shares."""
        # First, buy some shares to own them
        symbol = 'TSLA'
        buy_quantity = 5
        buy_price = MOCK_PRICES[symbol]
        buy_cost = buy_quantity * buy_price
        self.account.buy_shares(symbol, buy_quantity)

        # Now, sell a portion of them
        sell_quantity = 2
        sell_price = MOCK_PRICES[symbol] # Use mock price for sale
        sell_revenue = sell_quantity * sell_price

        self.account.sell_shares(symbol, sell_quantity)

        self.assertEqual(self.account.balance, self.initial_deposit - buy_cost + sell_revenue)
        self.assertEqual(self.account.holdings.get(symbol), buy_quantity - sell_quantity)
        self.assertEqual(len(self.account.transactions), 2) # One buy, one sell
        tx = self.account.transactions[-1] # Get the last transaction (the sell)
        self.assertEqual(tx['type'], TransactionType.SELL)
        self.assertEqual(tx['symbol'], symbol)
        self.assertEqual(tx['quantity'], sell_quantity)
        self.assertEqual(tx['amount'], sell_revenue) # Amount here represents the total revenue
        self.assertAlmostEqual(tx['balance_after'], self.initial_deposit - buy_cost + sell_revenue, places=2)

    def test_sell_shares_insufficient_holdings(self):
        """Test attempting to sell more shares than currently owned."""
        symbol = 'AAPL'
        buy_quantity = 5
        self.account.buy_shares(symbol, buy_quantity)

        sell_quantity = 10 # Trying to sell more than owned
        with self.assertRaisesRegex(ValueError, "Insufficient shares to sell. You have .* shares of .* but tried to sell .*"):
            self.account.sell_shares(symbol, sell_quantity)
        self.assertEqual(self.account.holdings.get(symbol), buy_quantity) # Holdings should remain unchanged
        self.assertEqual(self.account.balance, self.initial_deposit - (buy_quantity * MOCK_PRICES[symbol])) # Balance should remain unchanged

    def test_sell_shares_invalid_symbol(self):
        """Test selling shares of a symbol not held by the account."""
        symbol = 'MSFT' # Not bought
        quantity = 5
        with self.assertRaisesRegex(ValueError, "Insufficient shares to sell."): # Message is generic if symbol not in holdings
            self.account.sell_shares(symbol, quantity)
        self.assertNotIn(symbol, self.account.holdings) # Should not be in holdings

    def test_sell_shares_invalid_quantity_zero(self):
        """Test selling shares with zero quantity."""
        symbol = 'AAPL'
        self.account.buy_shares(symbol, 10) # Buy some first
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.sell_shares(symbol, 0)
        self.assertEqual(self.account.holdings.get(symbol), 10) # Holdings unchanged

    def test_sell_shares_invalid_quantity_negative(self):
        """Test selling shares with negative quantity."""
        symbol = 'AAPL'
        self.account.buy_shares(symbol, 10)
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.sell_shares(symbol, -5)
        self.assertEqual(self.account.holdings.get(symbol), 10) # Holdings unchanged

    def test_sell_shares_invalid_quantity_float(self):
        """Test selling shares with non-integer quantity."""
        symbol = 'AAPL'
        self.account.buy_shares(symbol, 10)
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.sell_shares(symbol, 5.5)
        self.assertEqual(self.account.holdings.get(symbol), 10) # Holdings unchanged

    def test_sell_shares_invalid_symbol_type(self):
        """Test selling shares with non-string symbol type."""
        symbol = 54321 # Invalid type
        quantity = 10
        with self.assertRaisesRegex(ValueError, "Share symbol must be a non-empty string."):
            self.account.sell_shares(symbol, quantity)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_sell_shares_empty_symbol(self):
        """Test selling shares with empty string symbol."""
        symbol = ""
        quantity = 10
        with self.assertRaisesRegex(ValueError, "Share symbol must be a non-empty string."):
            self.account.sell_shares(symbol, quantity)
        self.assertEqual(self.account.balance, self.initial_deposit)

    def test_sell_all_shares_of_symbol(self):
        """Test selling all owned shares of a specific symbol."""
        symbol = 'GOOGL'
        quantity = 3
        self.account.buy_shares(symbol, quantity)
        
        initial_balance_after_buy = self.account.balance
        sell_revenue = quantity * MOCK_PRICES[symbol]

        self.account.sell_shares(symbol, quantity)

        self.assertEqual(self.account.balance, initial_balance_after_buy + sell_revenue)
        self.assertNotIn(symbol, self.account.holdings) # Should be removed from holdings
        self.assertEqual(len(self.account.transactions), 2) # One buy, one sell

    # --- Portfolio Value Tests ---
    def test_get_portfolio_value_empty(self):
        """Test portfolio value when the account has no holdings."""
        self.assertEqual(self.account.get_portfolio_value(), 0.0)

    def test_get_portfolio_value_with_holdings(self):
        """Test portfolio value calculation with multiple holdings."""
        self.account.buy_shares('AAPL', 10) # 10 * 170 = 1700
        self.account.buy_shares('TSLA', 5)  # 5 * 250 = 1250
        
        expected_value = (10 * MOCK_PRICES['AAPL']) + (5 * MOCK_PRICES['TSLA'])
        self.assertAlmostEqual(self.account.get_portfolio_value(), expected_value, places=2)

    def test_get_portfolio_value_after_sell(self):
        """Test portfolio value after selling some shares."""
        self.account.buy_shares('AAPL', 10) # 1700
        self.account.buy_shares('TSLA', 5)  # 1250
        self.account.sell_shares('AAPL', 5) # Sell 5 AAPL, revenue: 5 * 170 = 850

        # Remaining holdings: 5 AAPL, 5 TSLA
        expected_value = (5 * MOCK_PRICES['AAPL']) + (5 * MOCK_PRICES['TSLA'])
        self.assertAlmostEqual(self.account.get_portfolio_value(), expected_value, places=2)

    # --- Total Value Tests ---
    def test_get_total_value_initial(self):
        """Test total value with only initial cash balance."""
        self.assertAlmostEqual(self.account.get_total_value(), self.initial_deposit, places=2)

    def test_get_total_value_with_holdings(self):
        """Test total value calculation including cash and portfolio."""
        self.account.buy_shares('AAPL', 10) # Cost: 1700. Balance: 8300.
        # Holdings: AAPL: 10, Value: 10 * 170 = 1700
        # Total Value = Balance + Portfolio Value = 8300 + 1700 = 10000
        self.assertAlmostEqual(self.account.get_total_value(), self.initial_deposit, places=2)

    def test_get_total_value_after_sell_and_deposit(self):
        """Test total value after sell and deposit."""
        # Initial Deposit: 10000
        # Buy 10 AAPL: Cost: 1700. Balance: 10000 - 1700 = 8300. Holdings: AAPL: 10
        self.account.buy_shares('AAPL', 10) 
        # Sell 5 AAPL: Revenue: 850. Balance: 8300 + 850 = 9150. Holdings: AAPL: 5
        self.account.sell_shares('AAPL', 5) 
        # Deposit 1000: Balance: 9150 + 1000 = 10150. Holdings: AAPL: 5
        self.account.deposit(1000)

        # Current state: Balance = 10150
        # Holdings: AAPL: 5, Portfolio Value = 5 * 170 = 850
        # Total Value = Balance + Portfolio Value = 10150 + 850 = 11000
        expected_total_value = 11000.0
        self.assertAlmostEqual(self.account.get_total_value(), expected_total_value, places=2)

    # --- Profit/Loss Tests ---
    def test_get_profit_loss_initial_state(self):
        """Test P/L calculation when only initial deposit exists (should be 0)."""
        self.assertAlmostEqual(self.account.get_profit_loss(), 0.0, places=2)

    def test_get_profit_loss_after_buy_same_price(self):
        """Test P/L after buying shares at the same price as mock price (should be 0)."""
        symbol = 'AAPL'
        quantity = 10
        self.account.buy_shares(symbol, quantity)
        # Since buy price == mock price and no sell occurs, P/L should still be 0
        # as total_value == initial_deposit
        self.assertAlmostEqual(self.account.get_profit_loss(), 0.0, places=2)

    def test_get_profit_loss_after_sell_at_profit(self):
        """Test P/L after selling shares at a profit (simulated price increase)."""
        symbol = 'GOOGL'
        quantity = 2
        buy_cost = quantity * MOCK_PRICES[symbol] # 2 * 1500 = 3000
        self.account.buy_shares(symbol, quantity) # Balance: 10000 - 3000 = 7000

        # Simulate a price increase for selling
        def mock_price_increase(sym):
            if sym == 'GOOGL':
                return MOCK_PRICES[sym] * 1.1 # 10% increase, 1500 * 1.1 = 1650
            return MOCK_PRICES.get(sym, 0.0)
        
        self.mock_get_share_price.side_effect = mock_price_increase
        
        sell_revenue = quantity * mock_price_increase(symbol) # 2 * 1650 = 3300
        self.account.sell_shares(symbol, quantity) # Balance: 7000 + 3300 = 10300

        # Total Value = 10300 (cash) + 0 (holdings gone) = 10300
        # P/L = Total Value - Initial Deposit = 10300 - 10000 = 300
        expected_pl = sell_revenue - buy_cost # This is the actual profit realized
        self.assertAlmostEqual(self.account.get_profit_loss(), expected_pl, places=2)

    def test_get_profit_loss_after_sell_at_loss(self):
        """Test P/L after selling shares at a loss (simulated price decrease)."""
        symbol = 'MSFT'
        quantity = 10
        buy_cost = quantity * MOCK_PRICES[symbol] # 10 * 300 = 3000
        self.account.buy_shares(symbol, quantity) # Balance: 10000 - 3000 = 7000

        # Simulate a price decrease for selling
        def mock_price_decrease(sym):
            if sym == 'MSFT':
                return MOCK_PRICES[sym] * 0.9 # 10% decrease, 300 * 0.9 = 270
            return MOCK_PRICES.get(sym, 0.0)
        
        self.mock_get_share_price.side_effect = mock_price_decrease
        
        sell_revenue = quantity * mock_price_decrease(symbol) # 10 * 270 = 2700
        self.account.sell_shares(symbol, quantity) # Balance: 7000 + 2700 = 9700

        # Total Value = 9700 (cash) + 0 (holdings gone) = 9700
        # P/L = Total Value - Initial Deposit = 9700 - 10000 = -300
        expected_pl = sell_revenue - buy_cost # This is the actual loss realized
        self.assertAlmostEqual(self.account.get_profit_loss(), expected_pl, places=2)

    def test_get_profit_loss_with_unrealized_gain(self):
        """Test P/L with unrealized gain (holdings value > cost basis)."""
        buy_symbol = 'AAPL'
        buy_quantity = 5
        buy_cost = buy_quantity * MOCK_PRICES[buy_symbol] # 5 * 170 = 850
        self.account.buy_shares(buy_symbol, buy_quantity) # Balance: 10000 - 850 = 9150

        # Simulate a price increase for holdings valuation
        def mock_price_increase(sym):
            if sym == 'AAPL':
                return MOCK_PRICES[sym] * 1.2 # 20% increase, 170 * 1.2 = 204
            return MOCK_PRICES.get(sym, 0.0)
        
        self.mock_get_share_price.side_effect = mock_price_increase
        
        # Current holdings value: 5 * 204 = 1020
        # Current cash balance: 9150
        # Total Value = 9150 + 1020 = 10170
        # P/L = 10170 - 10000 = 170
        expected_pl = (10170.0) - self.initial_deposit
        self.assertAlmostEqual(self.account.get_profit_loss(), expected_pl, places=2)

    # --- Get Holdings Tests ---
    def test_get_holdings_empty_account(self):
        """Test get_holdings on an account with no shares."""
        self.assertEqual(self.account.get_holdings(), {})

    def test_get_holdings_after_buys(self):
        """Test get_holdings after buying multiple stocks."""
        self.account.buy_shares('AAPL', 10)
        self.account.buy_shares('TSLA', 5)
        expected = {'AAPL': 10, 'TSLA': 5}
        self.assertEqual(self.account.get_holdings(), expected)

    def test_get_holdings_after_sell(self):
        """Test get_holdings after selling some shares."""
        self.account.buy_shares('AAPL', 10)
        self.account.buy_shares('TSLA', 5)
        self.account.sell_shares('AAPL', 3)
        expected = {'AAPL': 7, 'TSLA': 5}
        self.assertEqual(self.account.get_holdings(), expected)

    def test_get_holdings_after_selling_all(self):
        """Test get_holdings after selling all shares of a stock."""
        self.account.buy_shares('AAPL', 10)
        self.account.sell_shares('AAPL', 10)
        self.assertNotIn('AAPL', self.account.holdings)
        self.assertEqual(self.account.get_holdings(), {})

    def test_get_holdings_returns_copy(self):
        """Test that get_holdings returns a copy, not the original dictionary."""
        self.account.buy_shares('AAPL', 10)
        holdings_copy = self.account.get_holdings()
        holdings_copy['AAPL'] = 100 # Modify the copy
        # Original holdings should remain unchanged
        self.assertEqual(self.account.holdings.get('AAPL'), 10)
        self.assertNotEqual(holdings_copy.get('AAPL'), self.account.holdings.get('AAPL'))

    # --- Get Transactions Tests ---
    def test_get_transactions_empty(self):
        """Test get_transactions on an account with no transactions."""
        self.assertEqual(self.account.get_transactions(), [])

    def test_get_transactions_after_operations(self):
        """Test get_transactions after various account operations."""
        self.account.deposit(1000)
        self.account.buy_shares('AAPL', 5)
        self.account.sell_shares('AAPL', 2)
        self.account.withdraw(500)

        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 4)
        
        # Check types and order
        self.assertEqual(transactions[0]['type'], TransactionType.DEPOSIT)
        self.assertEqual(transactions[1]['type'], TransactionType.BUY)
        self.assertEqual(transactions[2]['type'], TransactionType.SELL)
        self.assertEqual(transactions[3]['type'], TransactionType.WITHDRAWAL)
        
        # Check details of one transaction (e.g., the last one)
        self.assertEqual(transactions[3]['amount'], 500)
        self.assertIn('timestamp', transactions[3])

    def test_get_transactions_returns_copy(self):
        """Test that get_transactions returns a copy, not the original list."""
        self.account.deposit(100)
        transactions_list = self.account.get_transactions()
        transactions_list.append({"dummy_tx": True}) # Modify the returned list
        # Original transactions list should remain unchanged
        self.assertEqual(len(self.account.transactions), 1)
        self.assertNotEqual(len(transactions_list), len(self.account.transactions))

    # --- Get Account Summary Tests ---
    def test_get_account_summary_initial_state(self):
        """Test the account summary for a newly created account."""
        summary = self.account.get_account_summary()
        self.assertEqual(summary['account_id'], self.account_id)
        self.assertAlmostEqual(summary['cash_balance'], self.initial_deposit, places=2)
        self.assertAlmostEqual(summary['portfolio_value'], 0.0, places=2)
        self.assertAlmostEqual(summary['total_value'], self.initial_deposit, places=2)
        self.assertAlmostEqual(summary['profit_loss'], 0.0, places=2)
        self.assertAlmostEqual(summary['initial_deposit'], self.initial_deposit, places=2)

    def test_get_account_summary_after_trades(self):
        """Test the account summary after performing buy and sell operations."""
        # Initial Deposit: 10000
        # Buy 10 AAPL: Cost: 1700. Balance: 10000 - 1700 = 8300. Holdings: AAPL: 10
        self.account.buy_shares('AAPL', 10) 
        # Buy 2 TSLA: Cost: 500. Balance: 8300 - 500 = 7800. Holdings: AAPL: 10, TSLA: 2
        self.account.buy_shares('TSLA', 2)  
        # Sell 5 AAPL: Revenue: 850. Balance: 7800 + 850 = 8650. Holdings: AAPL: 5, TSLA: 2
        self.account.sell_shares('AAPL', 5) 

        summary = self.account.get_account_summary()
        
        expected_cash_balance = 8650.0
        
        # Holdings: 5 AAPL, 2 TSLA
        # Portfolio Value: (5 * 170) + (2 * 250) = 850 + 500 = 1350.0
        expected_portfolio_value = 1350.0

        # Total Value = Cash Balance + Portfolio Value = 8650.0 + 1350.0 = 10000.0
        expected_total_value = expected_cash_balance + expected_portfolio_value
        
        # Profit/Loss = Total Value - Initial Deposit = 10000.0 - 10000.0 = 0.0
        expected_pl = expected_total_value - self.initial_deposit

        self.assertAlmostEqual(summary['cash_balance'], expected_cash_balance, places=2)
        self.assertAlmostEqual(summary['portfolio_value'], expected_portfolio_value, places=2)
        self.assertAlmostEqual(summary['total_value'], expected_total_value, places=2)
        self.assertAlmostEqual(summary['profit_loss'], expected_pl, places=2)
        self.assertAlmostEqual(summary['initial_deposit'], self.initial_deposit, places=2)


if __name__ == '__main__':
    # This allows running the tests directly from the command line.
    # unittest.main() is typically used, but for environments where sys.argv
    # might be manipulated (like some notebooks), passing explicit arguments is safer.
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
```