from .new_transaction import new_transaction, input_date
from .get_transaction import print_log
from .delete_transaction import delete_entry
from database import TransactionDB, BalanceDB

date_format = "%d-%m-%Y"

def add_transaction() -> None:
    tran = new_transaction(date_format)
    TransactionDB().add_entry(tran)
    BalanceDB().update_balance(tran)
    
def show_log() -> None:
    print("Specify the dates of the transactions that should be showed in the log:", end="\n\n")
    start_date = input_date(date_format, "Please enter the start date (DD-MM-YYYY):  ")
    end_date = input_date(date_format, "Please enter the end date (DD-MM-YYYY):  ")
    print("")
    print_log(start_date, end_date, date_format, summary=True)

def delete_transaction() -> None:
    date = input_date(date_format, "Please enter the date of the transaction to be deleted (DD-MM-YYYY):  ")
    delete_entry(date, date_format)
    