class Account:
    def __init__(self, account_number, account_holder_name, balance=0):
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited {amount} units. Current balance: {self.balance}"
        else:
            return "Invalid deposit amount."

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return f"Withdrew {amount} units. Current balance: {self.balance}"
        else:
            return "Insufficient funds or invalid withdrawal amount."

    def check_balance(self):
        return f"Current balance: {self.balance}"

    def display_account_details(self):
        return f"Account Number: {self.account_number}, Account Holder: {self.account_holder_name}, Balance: {self.balance}"


class SavingsAccount(Account):
    pass  # No additional functionality, inherits from Account


class CurrentAccount(Account):
    def __init__(self, account_number, account_holder_name, overdraft_limit, balance=0):
        super().__init__(account_number, account_holder_name, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        total_funds = self.balance + self.overdraft_limit
        if 0 < amount <= total_funds:
            self.balance -= amount
            return f"Withdrew {amount} units. Current balance: {self.balance}"
        else:
            return "Overdraft limit reached!"


# Example Usage
savings_account = SavingsAccount(account_number="12345", account_holder_name="Alice", balance=1000)
print(savings_account.deposit(500))  # Output: Deposited 500 units. Current balance: 1500
print(savings_account.withdraw(200))  # Output: Withdrew 200 units. Current balance: 1300
print(savings_account.check_balance())  # Output: Current balance: 1300
print(savings_account.display_account_details())  # Output: Account Number: 12345, Account Holder: Alice, Balance: 1300

current_account = CurrentAccount(account_number="67890", account_holder_name="Bob", overdraft_limit=3000, balance=5000)
print(current_account.withdraw(7000))  # Output: Withdrew 7000 units. Current balance: 2000
print(current_account.withdraw(9000))  # Output: Overdraft limit reached!
