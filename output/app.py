import gradio as gr
import datetime

# Assuming accounts.py is in the same directory
from accounts import Account, TransactionType, get_share_price

# --- Global state for simplicity (single user simulation) ---
# In a real app, you'd manage users and accounts more robustly.
user_account = None

def initialize_account(account_id: str, initial_deposit: float):
    """Initializes or resets the global user account."""
    global user_account
    try:
        user_account = Account(account_id, initial_deposit)
        return f"Account '{account_id}' created with initial deposit of ${initial_deposit:.2f}.", user_account.get_account_summary()
    except ValueError as e:
        return f"Error creating account: {e}", None

def get_account_instance():
    """Helper to ensure account is initialized before operations."""
    if user_account is None:
        raise gr.Error("Account not initialized. Please create an account first.")
    return user_account

# --- Gradio Interface Functions ---

def handle_create_account(account_id: str, initial_deposit: float):
    message, summary = initialize_account(account_id, initial_deposit)
    if summary:
        return message, str(summary).replace('{', '').replace('}', '').replace("'", "").replace(':', ': ')
    else:
        return message, "Account not created."

def handle_deposit(amount: float):
    try:
        account = get_account_instance()
        account.deposit(amount)
        return f"Deposit of ${amount:.2f} successful. Current balance: ${account.balance:.2f}", str(account.get_account_summary()).replace('{', '').replace('}', '').replace("'", "").replace(':', ': ')
    except ValueError as e:
        raise gr.Error(f"Deposit failed: {e}")
    except gr.Error as e:
        raise e

def handle_withdraw(amount: float):
    try:
        account = get_account_instance()
        account.withdraw(amount)
        return f"Withdrawal of ${amount:.2f} successful. Current balance: ${account.balance:.2f}", str(account.get_account_summary()).replace('{', '').replace('}', '').replace("'", "").replace(':', ': ')
    except ValueError as e:
        raise gr.Error(f"Withdrawal failed: {e}")
    except gr.Error as e:
        raise e

def handle_buy_shares(symbol: str, quantity: int):
    try:
        account = get_account_instance()
        account.buy_shares(symbol, quantity)
        current_price = get_share_price(symbol)
        cost = current_price * quantity
        return f"Bought {quantity} shares of {symbol} @ ${current_price:.2f} each. Total cost: ${cost:.2f}. New balance: ${account.balance:.2f}", str(account.get_account_summary()).replace('{', '').replace('}', '').replace("'", "").replace(':', ': ')
    except ValueError as e:
        raise gr.Error(f"Buy shares failed: {e}")
    except gr.Error as e:
        raise e

def handle_sell_shares(symbol: str, quantity: int):
    try:
        account = get_account_instance()
        account.sell_shares(symbol, quantity)
        current_price = get_share_price(symbol)
        revenue = current_price * quantity
        return f"Sold {quantity} shares of {symbol} @ ${current_price:.2f} each. Total revenue: ${revenue:.2f}. New balance: ${account.balance:.2f}", str(account.get_account_summary()).replace('{', '').replace('}', '').replace("'", "").replace(':', ': ')
    except ValueError as e:
        raise gr.Error(f"Sell shares failed: {e}")
    except gr.Error as e:
        raise e

def format_transactions(transactions):
    """Formats the transaction list for display."""
    if not transactions:
        return "No transactions yet."
    formatted = []
    for tx in transactions:
        details = f"{tx['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} | {tx['type']} | "
        if tx.get('symbol'):
            details += f"Symbol: {tx['symbol']}, Qty: {tx['quantity']}, "
        if tx.get('amount') is not None:
            details += f"Amount: ${tx['amount']:.2f}, "
        details += f"Balance After: ${tx['balance_after']:.2f} | Desc: {tx['description']}"
        formatted.append(details)
    return "\n".join(formatted)

def update_account_display():
    """Updates all relevant display components."""
    try:
        account = get_account_instance()
        summary = account.get_account_summary()
        holdings_str = str(account.get_holdings()).replace('{', '').replace('}', '').replace("'", "").replace(':', ': ')
        transactions_str = format_transactions(account.get_transactions())
        profit_loss_str = f"Total Profit/Loss: ${account.get_profit_loss():.2f}"
        return (str(summary).replace('{', '').replace('}', '').replace("'", "").replace(':', ': '),
                holdings_str,
                transactions_str,
                profit_loss_str)
    except gr.Error as e:
        # Return empty or default values if account not initialized
        return "Account not initialized.", "{}", "No transactions yet.", "Total Profit/Loss: $0.00"

# --- Gradio UI Definition ---

with gr.Blocks() as app:
    gr.Markdown("# Trading Simulation Account Manager")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## Account Management")
            account_id_input = gr.Textbox(label="Account ID", placeholder="Enter a unique ID")
            initial_deposit_input = gr.Number(label="Initial Deposit ($)", value=0.0, minimum=0)
            create_account_btn = gr.Button("Create/Reset Account")

            gr.Markdown("---")
            gr.Markdown("## Fund Operations")
            deposit_amount_input = gr.Number(label="Amount to Deposit ($)", minimum=0.01)
            deposit_btn = gr.Button("Deposit")
            withdraw_amount_input = gr.Number(label="Amount to Withdraw ($)", minimum=0.01)
            withdraw_btn = gr.Button("Withdraw")

            gr.Markdown("---")
            gr.Markdown("## Share Trading")
            share_symbol_input = gr.Textbox(label="Share Symbol (e.g., AAPL, TSLA, GOOGL)", placeholder="Enter symbol")
            share_quantity_input = gr.Number(label="Quantity", value=1, minimum=1, precision=0) # Integer quantity
            buy_shares_btn = gr.Button("Buy Shares")
            sell_shares_btn = gr.Button("Sell Shares")

        with gr.Column(scale=2):
            gr.Markdown("## Account Dashboard")
            account_summary_output = gr.Textbox(label="Account Summary", lines=7, interactive=False)
            holdings_output = gr.Textbox(label="Current Holdings", lines=3, interactive=False)
            profit_loss_output = gr.Textbox(label="Profit/Loss", lines=1, interactive=False)
            transaction_history_output = gr.Textbox(label="Transaction History", lines=10, interactive=False)

    # --- Event Listeners ---
    create_account_btn.click(
        handle_create_account,
        inputs=[account_id_input, initial_deposit_input],
        outputs=[app.get_state(user_account), account_summary_output] # Use app.get_state to update the global user_account state if needed, though direct modification is done
    )
    # We need a way to trigger updates after other operations. A separate update button or dynamic updates are options.
    # For simplicity, we'll update after each operation for now.

    deposit_btn.click(
        handle_deposit,
        inputs=[deposit_amount_input],
        outputs=[app.get_state(user_account), account_summary_output] # Re-evaluate state and summary
    ).then(
        update_account_display,
        outputs=[account_summary_output, holdings_output, transaction_history_output, profit_loss_output]
    )

    withdraw_btn.click(
        handle_withdraw,
        inputs=[withdraw_amount_input],
        outputs=[app.get_state(user_account), account_summary_output] # Re-evaluate state and summary
    ).then(
        update_account_display,
        outputs=[account_summary_output, holdings_output, transaction_history_output, profit_loss_output]
    )

    buy_shares_btn.click(
        handle_buy_shares,
        inputs=[share_symbol_input, share_quantity_input],
        outputs=[app.get_state(user_account), account_summary_output] # Re-evaluate state and summary
    ).then(
        update_account_display,
        outputs=[account_summary_output, holdings_output, transaction_history_output, profit_loss_output]
    )

    sell_shares_btn.click(
        handle_sell_shares,
        inputs=[share_symbol_input, share_quantity_input],
        outputs=[app.get_state(user_account), account_summary_output] # Re-evaluate state and summary
    ).then(
        update_account_display,
        outputs=[account_summary_output, holdings_output, transaction_history_output, profit_loss_output]
    )

    # Initial load of dashboard components (will show 'Account not initialized')
    app.load(
        update_account_display,
        outputs=[account_summary_output, holdings_output, transaction_history_output, profit_loss_output]
    )

if __name__ == "__main__":
    # To run this Gradio app, save it as app.py in the same directory as accounts.py
    # and run `gradio app.py` from your terminal.
    app.launch()