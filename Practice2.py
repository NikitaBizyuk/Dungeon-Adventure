# Static attributes
# a static attribute is an attribute that belongs to the class itself, not 
# to any specific instance of that class. 


class User:
    user_count = 0 # static attribute

    def __init__(self, username, email, password): # instance attribute
        self.username = username
        self._email = email 
        self.password = password
        User.user_count += 1

    def display_user(self):
        print(f"Username: {self.username}, Email: {self._email}")


    @property # with properties you dont need to worry about creating getter . much less verbose.
    def email(self): # this is a getter
        print("Email Accessed")
        return self._email
    
    @email.setter
    def email(self, new_email):
        if "@" in new_email:
            self._email = new_email

    
user1 = User("COLLssdfO", "@gmail.com", "whywhywhy")
user2 = User("COLLO", "@gmail.com", "whywhywhy")
print(User.user_count)
print(user1.user_count)
print(user2.user_count)
# user1 = User("COLLO", "@gmail.com", "whywhywhy")
# print(user1.email)
# user1.email = "fjskdfjklsd@@" # this assignment statement uses the setter method above
# print(user1.email)

# Static attributes
# a static attribute is an attribute that belongs to the class itself, not 
# to any specific instance of that class. 

# use static methods for utility functions/ when does not need acces to instance data

class BankAccount:
    MIN_BALANCE = 100
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self._balance = balance

    def deposit(self, amount):
        if self._is_valid_amount(amount):
            self._balance += amount
            self.__log_transaction("deposit",amount)
        else :
            print("Deposit amount must be positive.")

    @staticmethod
    def is_valid_interest_rate(rate):
        return 0 <= rate <=5
    def _is_valid_amount(self, amount):
        return amount > 0



    def __log_transaction(self, transaction_type, amount):
        print(f"Logging the: {transaction_type} of $ {amount}. New Balance: $ {self._balance} ")
    
account = BankAccount("COLLINS", 7935)
account.deposit(200)
print(BankAccount.is_valid_interest_rate(3))
print(BankAccount.is_valid_interest_rate(10))








