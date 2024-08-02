from rich import print
import pandas as pd
from datetime import datetime
import ast

from database import TransactionDB

def select_category(categories: dict) -> str:
    categories = ast.literal_eval(categories)
    for key, value in categories.items():
        if value==1:
            return key
    return "Multiple"
    
def print_log(start_date: str, end_date: str, date_format: str, summary: bool = False) -> None:
    df = pd.read_csv(TransactionDB().filename)
    df["date"] = pd.to_datetime(df["date"], format=date_format)
    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)
    
    mask = (df["date"]>=start_date) & (df["date"]<=end_date)
    
    filtered_df = df.loc[mask]
    if filtered_df.empty:
        print("[bold yellow]WARNING:[/bold yellow] No transactions meet the specified criteria", end="\n\n")
        return
    print(f"Transactions from the [bold yellow]{start_date.strftime(date_format)}[/bold yellow] to the [bold yellow]{end_date.strftime(date_format)}[/bold yellow]:", end="\n\n")
    print(
        filtered_df.to_string(
index=False, formatters={"date": lambda x: x.strftime(date_format), "type": lambda x: "Income" if x else "Expense", "category": lambda x: select_category(x)}
        )
    )
    print("")
    
    if summary:
        income = filtered_df[filtered_df["type"]==True]["amount"].sum()
        expense = filtered_df[filtered_df["type"]==False]["amount"].sum()
        print("[bold underline]SUMMARY:[/bold underline]", end="\n\n")
        print(f"[green]INCOME:[/green]      {income:>10.2f}")
        print(f"[red]EXPENSE:[/red]:  {expense:>12.2f}")
        print(f"[yellow bold]NET SAVINGS: {(income-expense):>10.2f}[/yellow bold]", end="\n\n")
    return
    