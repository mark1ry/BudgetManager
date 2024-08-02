from rich import print
import os
from quotes import Quotes

from .transaction_dialogue import transaction_dialogue
from database import BalanceDB

def greeting() -> None:
    print("\n            Welcome to the [blue bold underline]BUDGET MANAGER[/blue bold underline]\n")
    print("It is great having you back today!", end="\n\n")
    
    quote = Quotes().random()
    print(f"{quote[1]} [magenta]- [bold]{quote[0]}[/bold][/magenta]", end="\n\n")  

def print_balance() -> None:
    balance = BalanceDB().read_balance()
    
    print("[underline]Your [bold]current balance[/bold] is the following:[/underline]", end="\n\n")
    label = "TOTAL:"
    value = balance["Total"]
    print(f"[bold][blue]{label.ljust(16)}[/blue][green]{round(value,2):>15.2f} €[/green][/bold]")
    for key, value in balance.items():
        if key=="Total":
            print("")
            continue
        label = key+":"
        print(f"[bold]{label.ljust(16)}[/bold][yellow]{round(value,2):>15.2f} €[/yellow]")
    print("")
    
def main_dialogue() -> None:
    print_balance()
    print("[bold]What section do you want to access?[/bold]", end="\n\n")
    print("[bold red]1.[/bold red] Transactions")
    print("[bold red]2.[/bold red] Debt")
    print("[bold red]3.[/bold red] Invest")
    print("[bold red]4.[/bold red] Exit Budget Manager")
    print("")
    try:
        option = int(input("Please select an option:  "))
        print("")
        if option==1:
            print("You entered the [bold green]Transactions[/bold green] section", end="\n\n")
            transaction_dialogue()
            main_dialogue()
        elif option==2:
            main_dialogue()
        elif option==3:
            main_dialogue()
        elif option==4:
            print("[bold blue]The [underline]BUDGET MANAGER[/underline] has been exited succesfully. See you next time![/bold blue]")
            return
        else:
            raise ValueError
    except ValueError:
        print("[bold red]ERROR:[/bold red] The value passed was not valid. Please try again.", end="\n\n")
        main_dialogue()

def clear_console() -> None:

    os.system('cls' if os.name == 'nt' else 'clear')