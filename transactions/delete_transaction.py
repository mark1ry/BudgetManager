from rich import print
import pandas as pd
from datetime import datetime
import ast

from database import TransactionDB, BalanceDB
from .transaction import Transaction
from .get_transaction import select_category

def get_entry_index(length: int) -> int:
    try:
        value = int(input("Please enter the index of the transaction to be deleted:  "))
        if value not in list(range(1, length+1)):
            raise ValueError
        print("")
        return value
    except ValueError:
        print("[bold red]ERROR:[/bold red] The index entered was not valid, please try again.", end="\n\n")
        return get_entry_index(length)
        
def subtract_balance(df: pd.DataFrame, index: int, date_format: str) -> None:
    entry = df.loc[index]
    trans = Transaction(entry["date"], (entry["amount"]*-1), entry["type"], ast.literal_eval(entry["category"]), entry["description"])
    BalanceDB().update_balance(trans)
    
    
def delete_entry(date: str, date_format: str) -> None:
    df = pd.read_csv(TransactionDB().filename)
    
    temp_df = pd.DataFrame()
    temp_df.insert(0, "date", pd.to_datetime(df["date"], format=date_format), True)
    date = datetime.strptime(date, date_format)
    
    mask = (temp_df["date"]>=date) & (temp_df["date"]<=date)
    
    filtered_df = df.loc[mask]
    filtered_length = sum(mask)
    filtered_df.insert(0, "index", list(range(1, filtered_length+1)), True)
    if filtered_df.empty:
        print("[bold yellow]WARNING:[/bold yellow] No transactions meet the specified criteria", end="\n\n")
        return
    print(f"Transactions from the [bold yellow]{date.strftime(date_format)}[/bold yellow] to the [bold yellow]{date.strftime(date_format)}[/bold yellow]:", end="\n\n")
    print(
        filtered_df.to_string(
            index=False, formatters={"type": lambda x: "Income" if x else "Expense", "category": lambda x: select_category(x)}
        )
    )
    print("")
    index = get_entry_index(filtered_length)    
    
    temp = 1
    for i in range(len(mask)):
        if mask[i]:
            if temp==index:
                mask[i] = False
                subtract_balance(filtered_df, i, date_format)
            else:
                mask[i] = True
            temp += 1
        else:
            mask[i] = True
    
    new_df = df.loc[mask]
    new_df.to_csv(TransactionDB().filename, index=False)
    print("[bold green]INFO:[/bold green] Transaction deleted successfully", end="\n\n")
    return
                

