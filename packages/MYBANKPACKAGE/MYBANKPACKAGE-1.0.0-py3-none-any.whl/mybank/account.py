#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Account:
    def __init__(self, account_number, account_holder_name, initial_balance=0):
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("Invalid withdrawal amount or insufficient funds.")

    def check_balance(self):
        return self.balance


# In[2]:


# Create an instance of the Account class
account1 = Account("12345", "John Doe", 1000)


# In[3]:


# Deposit money into the account
account1.deposit(500)


# In[4]:


# Withdraw money from the account
account1.withdraw(300)


# In[5]:


# Check the current balance
balance = account1.check_balance()
print(f"Account Balance: ${balance}")


# In[6]:


class AccountNumberAlreadyExists(Exception):
    def __init__(self, account_number):
        super().__init__(f"Account with number {account_number} already exists.")

class Account:
    account_numbers = set()  # Class-level variable to store unique account numbers

    def __init__(self, account_number, account_holder_name, initial_balance=0):
        if account_number in Account.account_numbers:
            raise AccountNumberAlreadyExists(account_number)
        
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.balance = initial_balance

        # Add the new account number to the class variable
        Account.account_numbers.add(account_number)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("Invalid withdrawal amount or insufficient funds.")

    def check_balance(self):
        return self.balance

    @classmethod
    def get_all_account_numbers(cls):
        return list(cls.account_numbers)


# In[7]:


# Example usage:

# Creating two accounts with different account numbers
account1 = Account("12345", "John Doe", 1000)
account2 = Account("67890", "Jane Smith", 500)

# Try to create another account with an existing account number (will raise an exception)
account3 = Account("12345", "Alice Johnson", 200)


# In[8]:


# Get all account numbers
all_account_numbers = Account.get_all_account_numbers()
print("All Account Numbers:", all_account_numbers)


# In[9]:


class Account:
    def __init__(self, account_number, account_holder_name, initial_balance=0):
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("Invalid withdrawal amount or insufficient funds.")

    def check_balance(self):
        return self.balance

class SavingsAccount(Account):
    # Inheriting from the base Account class
    pass

class CurrentAccount(Account):
    def __init__(self, account_number, account_holder_name, initial_balance=0, overdraft_limit=0):
        super().__init__(account_number, account_holder_name, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0 and amount <= (self.balance + self.overdraft_limit):
            self.balance -= amount
        else:
            print("Overdraft limit reached!")


# In[10]:


# Example usage:

# Create a Savings Account
savings_account = SavingsAccount("12345", "John Doe", 1000)

# Deposit and withdraw from the Savings Account
savings_account.deposit(500)
savings_account.withdraw(300)

# Check the balance of the Savings Account
print("Savings Account Balance:", savings_account.check_balance())


# In[11]:


# Create a Current Account with an overdraft limit of 3000
current_account = CurrentAccount("67890", "Jane Smith", 5000, overdraft_limit=3000)


# In[12]:


current_account.withdraw(7000)


# In[14]:


current_account.check_balance()


# In[15]:


current_account.withdraw(9000)


# In[ ]:




