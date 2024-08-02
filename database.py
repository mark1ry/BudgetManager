import pandas as pd
import csv
from rich import print
from transactions.transaction import Transaction

class Database:
    filename: str = ""
    
    def __init__(self, filename: str, columns: list):
        self.filename = filename
        if self.check_filename():
            database_read = False
            while not database_read:
                try:
                    pd.read_csv(self.filename)
                    database_read = True
                except:
                    self.create_database(columns)
    
    def check_filename(self) -> bool:
        if self.filename=="databases/transaction_database.csv" or self.filename=="databases/balance_database.csv":
            return True
        else:
            return False
    
    def create_database(self, columns: list) -> None:
        if columns==[]:
            balance = {
                "Total": 0.00,
                "Cost of living": 0.00,
                "Leisure": 0.00,
                "Savings": 0.00,
                "Education": 0.00,
                "Emergency": 0.00,
                "Investments": 0.00
            }
            with open(self.filename, "w") as csvfile:
                writer = csv.writer(csvfile)
                for key, value in balance.items():
                    writer.writerow([key,value])
        else:
            df = pd.DataFrame(columns=columns)
            df.to_csv(self.filename, index=False)        

class TransactionDB(Database):
    __columns: list = ["date", "amount", "type", "category", "description"]
    
    def __init__(self):
        super().__init__("databases/transaction_database.csv", self.__columns)
    
    def add_entry(self, entry: Transaction) -> None:
        new_entry={
            "date":entry.get_date(),
            "amount":entry.get_amount(),
            "type":entry.get_is_income(),
            "category":entry.get_category(),
            "description":entry.get_description()
        }
        with open(self.filename, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.__columns)
            writer.writerow(new_entry)
        print("[bold green]INFO:[/bold green] Entry added succesfully to the transaction record", end="\n\n")

class BalanceDB(Database):

    def __init__(self):
        super().__init__("databases/balance_database.csv", [])

    def update_balance(self, entry: Transaction) -> None:
        balance = self.read_balance()
        
        new_entry = [round(entry.get_amount(), 2),]
        temp = [value for value in entry.get_category().values()]
        temp = [round(new_entry[0]*element, 2) for element in temp]
        temp[0] += (new_entry[0]-sum(temp))
        for element in temp:
            new_entry.append(element)
        
        index = 0
        if entry.get_is_income()==True:
            for key, value in balance.items():
                balance[key] = round(value + new_entry[index],2)
                index += 1
        else:
            for key, value in balance.items():
                balance[key] = round(value - new_entry[index],2)
                index += 1
        
        with open(self.filename, "w") as csvfile:
                writer = csv.writer(csvfile)
                for key, value in balance.items():
                    writer.writerow([key,value])
        print("[bold green]INFO:[/bold green] Balance updated succesfully", end="\n\n")

    def read_balance(self) -> dict:
        balance = {}
        with open(self.filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row)!=2:
                    continue
                key, value = row
                balance[key] = float(value)
        return balance
