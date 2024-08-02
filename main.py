from database import TransactionDB, BalanceDB
from dialogue.main_dialogue import greeting, main_dialogue


def create_databases() -> None:
    TransactionDB()
    BalanceDB()

def run_program():
    create_databases()
    greeting()
    main_dialogue()
        
if __name__ == "__main__":
    run_program()