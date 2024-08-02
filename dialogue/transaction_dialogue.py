from rich import print
from transactions.actions import *

def transaction_dialogue() -> None:
    print("[bold]What action would you like to carry out?[/bold]", end="\n\n")
    print("[bold green]1.[/bold green] Add a new transaction")
    print("[bold green]2.[/bold green] Delete a transaction")
    print("[bold green]3.[/bold green] See log of transactions")
    print("[bold green]4.[/bold green] Exit Transactions")
    print("")
    try:
        option = int(input("Please choose an option:  "))
        print("")
        if option==1:
            add_transaction()
            return transaction_dialogue()
        elif option==2:
            delete_transaction()
            return transaction_dialogue()
        elif option==3:
            show_log()
            return transaction_dialogue()
        elif option==4:
            print("Successfully exited [bold]Transaction[/bold].", end="\n\n")
            return
        else:
            raise ValueError
    except ValueError:
        print("[bold red]ERROR:[/bold red] The value entered is invalid. Please try again.", end="\n\n")
        return transaction_dialogue()
        
