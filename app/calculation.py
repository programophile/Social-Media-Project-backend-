def add (a: int, b: 2) :
    return a + b


class BankAccount:
    def __init__(self,starting_balance: float = 0):
        self.balance = starting_balance 
    def deposit(self, amount: float):
        self.balance += amount  
    def withdraw(self, amount: float):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
    def collect_interest(self, interest_rate: float=1.1):
        self.balance += self.balance * interest_rate