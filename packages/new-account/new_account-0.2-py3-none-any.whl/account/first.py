import pandas as pd

class AccountNumberAlreadyExists(Exception):
    def __init__(self, acc_number):
        super().__init__(f"Account with number {acc_number} already exists.")


class MegaBank:

    existing_account_numbers = set()

    def __init__(self, acc_number, acc_name, balance):

        if acc_number in MegaBank.existing_account_numbers:
            raise AccountNumberAlreadyExists(acc_number)

        self.acc_number = acc_number
        self.acc_name = acc_name
        self.balance = balance
        MegaBank.existing_account_numbers.add(acc_number)

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
        else:
            raise ValueError ('deposit amount must be in positive')
        
    def withdraw(self, amount):
        if amount >= 0:
            self.balance -= amount
        else:
            raise ValueError('withdraw amount must be in positive')

    def check_balance(self):
        return self.balance




class SavingsAccount(MegaBank):
    pass


class CurrentAccount(MegaBank):

    def __init__(self, acc_number, acc_name, balance, overdraft_limit):
        super().__init__(acc_number, acc_name, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount>0 and amount <= (self.balance + self.overdraft_limit):
            if amount <= self.balance:
                self.balance -= amount
            else:
                self.overdraft_limit -= (amount -self.balance)
                self.balance = 0
            print(self.balance)
        else:
            print('Overdraft limit reached!')