import pandas,requests,os
#the class account is created
class Account:
    def __init__(self, account_number, account_holder_name, initial_balance=0.0):
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.balance = initial_balance
# deposit method is created
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited {amount} into the account. New balance: {self.balance}"
        else:
            return "Deposit amount must be positive."
# withdraw mehtod is created
    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return f"Withdrew {amount} from the account. New balance: {self.balance}"
        else:
            return "Insufficient funds for withdrawal."
# get_balance method is created
    def get_balance(self):
        return f"Current balance: {self.balance}"
 
class SavingsAccount(Account):
    # Inherits from the base Account class with no additional properties or methods
    pass
#the class CurrentAccount is created which inherits from Account parent class
class CurrentAccount(Account):
    def __init__(self, account_number, account_holder_name, initial_balance=0.0, overdraft_limit=0.0):
        # super keyword is used to used to inherit the init constructor from parent class
        super().__init__(account_number, account_holder_name, initial_balance)
        self.overdraft_limit = overdraft_limit
     # this is the overiding withdraw method
    def withdraw(self, amount):
        if amount > 0:
            available_balance = self.balance + self.overdraft_limit
            if amount <= available_balance:
                self.balance -= amount
                return f"Withdrew {amount} from the account. New balance: {self.balance}"
            else:
                return "Overdraft limit reached!"
        else:
            return "Withdrawal amount must be positive."
        
