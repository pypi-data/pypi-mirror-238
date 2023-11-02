# %%
class BankAccount:

     # Class variable to store all account numbers
    all_account_numbers = []

    def __init__(self, account_number, account_holder, balance):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance

         # Add the account number to the list
        BankAccount.all_account_numbers.append(account_number)

    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            raise ValueError("Deposit amount must be positive.")
    
    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
        else:
            raise ValueError("Withdrawal amount must be positive and within the account balance.")

    def get_balance(self):
        return self.balance
    
    @classmethod
    def get_all_account_numbers(cls):
        return cls.all_account_numbers



# %%
# Create an instance of the class
account1 = BankAccount(account_number=12345, account_holder="John Doe", balance = 30000)
account2 = BankAccount(account_number="54321", account_holder="Jane Smith", balance = 15000)

# Deposit and withdraw money
account1.deposit(1000)
account1.withdraw(500)
# Check the balance
print("Current balance:", account1.get_balance())

# %%
class SavingsAccount(BankAccount):
        pass
        # No need to extend or modify properties/methods

# %%
class CurrentAccount(BankAccount):
    def __init__(self, account_number, account_holder, balance=0, overdraft_limit=0):
        super().__init__(account_number, account_holder, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0:
            if self.balance + self.overdraft_limit >= amount:
                self.balance -= amount
            else:
                print("Overdraft limit reached!")
        else:
            print("Invalid withdrawal amount")

# %%
# Example usage
savings_account = SavingsAccount("12345", "John Doe", 5000)
current_account = CurrentAccount("54321", "Jane Smith", 5000, overdraft_limit=3000)

# %%
savings_account.withdraw(2000)
print("Savings Account Balance:", savings_account.get_balance())

current_account.withdraw(7000)
print("Current Account Balance:", current_account.get_balance())

current_account.withdraw(9000)
print("Current Account Balance:", current_account.get_balance())

# %%


# %%
# Access the list of all account numbers using the class method
all_account_numbers = BankAccount.get_all_account_numbers()

# Print the list of all account numbers
print("All account numbers:", all_account_numbers)

# %%
class AccountNumberAlreadyExists(Exception):
    def __init__(self, account_number):
        super().__init__(f"Account with number {account_number} already exists.")

# %%
existing_account_numbers = ['12345']
account_number = "12345"

# Check if the account number already exists
if account_number in existing_account_numbers:
    raise AccountNumberAlreadyExists(account_number) 

# %%
jupyter nbconvert --to script untiltled-1.ipynb

# %%



