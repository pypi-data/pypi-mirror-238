class BankTransactions():
   def deposit(self,name,account_number,account_name,cur_balance):
       self.deposit=int(input("Enter the amount to deposit"))
       if(self.deposit<0):
           print("Deposit is negative so cant be added")
       else:
           self.cur_balance=cur_balance+self.deposit
       print("The new Balance is",self.cur_balance)
   def withdrawal(self,name,account_number,account_name,cur_balance):
       self.withdrawal=int(input("Enter the amount to withdraw"))
       if(cur_balance<self.withdrawal):
           print("Can't Withdraw ")
       else:
           self.cur_balance=cur_balance-self.withdrawal
       print("The updated balance is ",self.cur_balance)
   def check_balance(self):
       print("The balance is",self.cur_balance)
obj1=BankTransactions()
obj1.deposit("Anirudh","1000000","SBIANIRUDH",50)
x=obj1.cur_balance
obj1.withdrawal("Anirudh","1000000","SBIANIRUDH",x)


class AccountCreationError(Exception):
    def __init__(self, account_number):
        self.account_number = account_number
        super().__init__(f"Account number {account_number} already exists.")


class BankAccount:
    # Class-level variable to store all created account numbers
    all_account_numbers = set()

    def __init__(self, account_number,account_name, balance=0):
        if account_number in BankAccount.all_account_numbers:
            raise AccountCreationError(account_number)
        self.account_number = account_number
        self.account_name= account_name
        self.balance = balance
        # Add the new account number to the set
        BankAccount.all_account_numbers.add(account_number)




