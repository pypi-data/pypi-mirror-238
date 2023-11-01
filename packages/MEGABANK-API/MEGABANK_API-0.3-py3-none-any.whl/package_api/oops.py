# create a class for accounts
class Account():
   
    def __init__(self, account_number, account_holder_name, balance=0):
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.balance = balance
    
    # Method to deposit money into the account
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
    
    # Method to withdraw money from the account
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
    
    # Method to get the current balance of the account
    def get_balance(self):
        return self.balance
    
obj1=Account(2809,'Dinesh',28000)

obj1.get_balance()

