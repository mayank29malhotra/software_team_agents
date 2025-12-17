import gradio as gr
from accounts import Account, get_share_price

account = None

def create_account(initial_balance):
    global account
    account = Account(initial_balance)
    return f"Account created with an initial balance of ${initial_balance}"

def deposit(amount):
    if account is None:
        return "Account does not exist. Please create an account first."
    account.deposit(amount)
    return f"Deposited ${amount}. New balance: ${account.balance}"

def withdraw(amount):
    if account is None:
        return "Account does not exist. Please create an account first."
    try:
        account.withdraw(amount)
        return f"Withdrew ${amount}. New balance: ${account.balance}"
    except ValueError as e:
        return str(e)

def buy_shares(symbol, quantity):
    if account is None:
        return "Account does not exist. Please create an account first."
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}. New holdings: {account.get_holdings()}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol, quantity):
    if account is None:
        return "Account does not exist. Please create an account first."
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}. New holdings: {account.get_holdings()}"
    except ValueError as e:
        return str(e)

def report_holdings():
    if account is None:
        return "Account does not exist. Please create an account first."
    return str(account.get_holdings())

def report_profit_loss():
    if account is None:
        return "Account does not exist. Please create an account first."
    return f"Profit/Loss: ${account.get_profit_loss()}"

def list_transactions():
    if account is None:
        return "Account does not exist. Please create an account first."
    return str(account.get_transactions())

with gr.Blocks() as demo:
    gr.Markdown("## Trading Simulation Platform")

    with gr.Row():
        create_balance_input = gr.Number(label="Initial Balance", value=1000, interactive=True)
        create_button = gr.Button("Create Account")

    create_output = gr.Textbox(label="Output", interactive=False)
    create_button.click(create_account, inputs=create_balance_input, outputs=create_output)

    deposit_input = gr.Number(label="Deposit Amount", interactive=True)
    deposit_button = gr.Button("Deposit")
    deposit_output = gr.Textbox(label="Output", interactive=False)
    deposit_button.click(deposit, inputs=deposit_input, outputs=deposit_output)

    withdraw_input = gr.Number(label="Withdraw Amount", interactive=True)
    withdraw_button = gr.Button("Withdraw")
    withdraw_output = gr.Textbox(label="Output", interactive=False)
    withdraw_button.click(withdraw, inputs=withdraw_input, outputs=withdraw_output)

    buy_symbol_input = gr.Textbox(label="Symbol to Buy")
    buy_quantity_input = gr.Number(label="Quantity to Buy", interactive=True)
    buy_button = gr.Button("Buy Shares")
    buy_output = gr.Textbox(label="Output", interactive=False)
    buy_button.click(buy_shares, inputs=[buy_symbol_input, buy_quantity_input], outputs=buy_output)

    sell_symbol_input = gr.Textbox(label="Symbol to Sell")
    sell_quantity_input = gr.Number(label="Quantity to Sell", interactive=True)
    sell_button = gr.Button("Sell Shares")
    sell_output = gr.Textbox(label="Output", interactive=False)
    sell_button.click(sell_shares, inputs=[sell_symbol_input, sell_quantity_input], outputs=sell_output)

    holdings_button = gr.Button("Report Holdings")
    holdings_output = gr.Textbox(label="Output", interactive=False)
    holdings_button.click(report_holdings, outputs=holdings_output)

    profit_loss_button = gr.Button("Report Profit/Loss")
    profit_loss_output = gr.Textbox(label="Output", interactive=False)
    profit_loss_button.click(report_profit_loss, outputs=profit_loss_output)

    transactions_button = gr.Button("List Transactions")
    transactions_output = gr.Textbox(label="Output", interactive=False)
    transactions_button.click(list_transactions, outputs=transactions_output)

if __name__ == "__main__":
    demo.launch()