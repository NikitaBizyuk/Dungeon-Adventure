# Encapsulation - bundling the data fields and methods into a single unit called a class
# helps in hiding the internal implementation details of a class by only 
# exposing necessary functionality to the outside world

class BadBankAccount:
    def __init__(self, balance):
        self.balance = balance

# account = BadBankAccount(0.0)
# account.balance = -1
# print(account.balance)

class BankAccount:
    def __init__(self):
        self._balance = 0.0

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        self._balance += amount
    def withdraw(self,amount):
        if amount <=0 :
            raise ValueError("Withdraw amount must be postive")
        if amount >= self._balance :
            raise ValueError("Insufficient funds.")
        self._balance -= amount

account = BankAccount()
print(account.balance)
account.deposit(1.99)
print(account.balance)
account.withdraw(100)
print(account.balance)
