
class Transaction:
    
    __date: str = ""
    __amount: float = 0
    __is_income: bool = True
    __category: dict = {
                      "Cost de vida": 0.,
                      "Oci mensual": 0.,
                      "Estalvi": 0.,
                      "Formació": 0.,
                      "Emergència": 0.,
                      "Inversió": 0.
                      }
    __description: str = ""
          
    def __init__(self, date: str, amount: float, is_income: bool, category: dict, description: str):
        self.__date = date
        self.__amount = amount
        self.__is_income = is_income
        self.__category = category
        self.__description = description
    
    def get_date(self) -> str:
        return self.__date
    
    def get_amount(self) -> float:
        return self.__amount
    
    def get_is_income(self) -> bool:
        return self.__is_income
    
    def get_category(self) -> dict:
        return self.__category
    
    def get_description(self) -> str:
        return self.__description