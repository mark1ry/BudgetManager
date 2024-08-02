from .transaction import Transaction
from rich import print
from rich.prompt import Prompt
from datetime import datetime

def input_date(date_format: str, prompt: str) -> str:  
    date = input(prompt)
    if not date:
        print("")
        return datetime.today().strftime(date_format)
    try:
        valid_date = datetime.strptime(date, date_format)
        print("")
        return valid_date.strftime(date_format)
    except ValueError:
        print("[red bold]ERROR[/red bold]: Invalid date format. Please enter the date in DD-MM-YYYY format.", end="\n\n")
        return input_date(date_format, prompt)
    
def input_amount() -> float:
    try:
        amount = float(input("What is the amount? (€):  "))
        if not amount>0:
            raise ValueError
        print("")
        return round(amount,2)
    except ValueError:
        print("[red bold]ERROR[/red bold]: The amount must be a non-negative and non-zero value", end="\n\n")
        return input_amount()

def input_type() -> bool:
    TYPES = {"I": True, "E": False}
    
    type = input("Is it an income or an expense? ('I' for Income or 'E' for Expense):  ").upper()
    if type in TYPES:
        print("")
        return TYPES[type]
    print("[bold red]ERROR[/bold red]: Invalid value. Please enter 'I' for Income or 'E' for Expense.", end="\n\n")
    return input_type()

def input_category(is_income: bool, categories: dict) -> dict:
    if is_income:
        return input_income_category(categories)
    else:
        return input_expense_category(categories)
    
def input_income_category(categories: dict) -> dict:
    print("How should the income be divided?", end="\n\n")
    print("[bold red]1.[/bold red] 55-15-15-5-10-0")
    print("[bold red]2.[/bold red] Personalized", end="\n\n")
    try:
        selected = int(input("Select the option by number:  "))
        if selected==1:
            categories["Cost of living"] = 0.55
            categories["Leisure"] = 0.15
            categories["Savings"] = 0.15
            categories["Education"] = 0.05
            categories["Emergency"] = 0.10
            categories["Investments"] = 0.00
            print("")
            return normalize_dict(categories)
        elif selected==2:
            print("")
            for key in categories.keys():
                categories[key] = ask_category(key)
            print("")
            return normalize_dict(categories)
        else:
            raise ValueError
    except ValueError:
        print("[bold red]ERROR[/bold red]: Please enter a number corresponding to one of the options.", end="\n\n")
        return input_income_category(categories)

def input_expense_category(categories: dict) -> dict:
    print("Choose the category of your expense:", end="\n\n")
    for index, key in enumerate(categories.keys()):
        print(f"[bold red]{index+1}.[/bold red] {key}")
    print("")
    try:
        selected = int(input("Select the category by number:  "))
        if selected not in list(range(1, len(list(categories.keys()))+1)):
            raise ValueError
        for index, key in enumerate(categories.keys()):
            if (index+1)==selected:
                categories[key] = 1.00
        print("")
        return categories
    except ValueError:
        print("[bold red]ERROR[/bold red]: Please enter a number corresponding to one of the categories.", end="\n\n")
        return input_expense_category(categories)

def ask_category(key: str) -> float:
    try:
        value = float(Prompt.ask(f"Enter the fraction corresponding to [bold green]{key}[/bold green]"))
        if value < 0:
            raise ValueError
        return value
    except ValueError:
        print("[bold red]ERROR[/bold red]: Please the fraction must be non-negative.")
        return ask_category(key)

def normalize_dict(dictionary: dict) -> dict:
    sum = 0.
    fraction_sum = 0.
    for value in dictionary.values():
        sum += value
    for key, value in dictionary.items():
        temp = round(value/sum, 2)
        dictionary[key] = temp
        fraction_sum += temp
    dictionary[list(dictionary.keys())[0]] += (1-fraction_sum)
    return dictionary
            
def input_description() -> str:
    return input("Enter the description (optional):  ")

def new_transaction(date_format: str) -> Transaction:
    categories = {
        "Cost of living": 0.,
        "Leisure": 0.,
        "Savings": 0.,
        "Education": 0.,
        "Emergency": 0.,
        "Investments": 0.  
    }
    
    date = input_date(date_format, "What is the date of the transaction? (DD-MM-YYYY or Enter for today's date):  ")
    amount = input_amount()
    is_income = input_type()
    categories = input_category(is_income, categories)
    description = input_description()
    print("")
    
    return Transaction(date, amount, is_income, categories, description)
       