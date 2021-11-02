class Category:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.ledger = []

    def __str__(self):
        res = ""

        res += "*" * ((30 - len(self.name)) // 2)
        res += self.name
        res += "*" * ((30 - len(self.name)) // 2)
        res += "\n"

        for txn in self.ledger:
            amount = f"{txn['amount']:.2f}"
            desc_length = 30 - len(amount)
            description = txn["description"][:desc_length - 1]
            res += description
            res += " " * (desc_length - len(description))
            res += amount
            res += "\n"
        
        res += f"Total: {self.balance:.2f}"
        return res

    def deposit(self, amount, description=""):
        self.balance += amount
        self.ledger.append({"amount": amount, "description": description})
    
    def check_funds(self, amount):
        return self.balance >= amount

    def withdraw(self, amount, description=""):
        if not self.check_funds(amount):
            return False

        self.balance -= amount
        self.ledger.append({"amount": -amount, "description": description})

        return True

    def transfer(self, amount, destination):
        if not self.check_funds(amount):
            return False
        
        self.withdraw(amount, f"Transfer to {destination.name}")
        destination.deposit(amount, f"Transfer from {self.name}")
        return True

    def get_balance(self):
        return self.balance


def create_spend_chart(categories):
    spending_list = []
    names = []
    for category in categories:
        spending_list.append(category.ledger[0]["amount"] - category.balance)
        names.append(category.name)

    total_spend = sum(spending_list)
    percentages = []
    for item in spending_list:
        percentage = (item / total_spend) * 100
        percentages.append(percentage // 10 * 10)

    res = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        if i < 100: res += " "
        if i < 10: res += " "
        res += f"{i}| "
        for item in percentages:
            res += "o" if item >= i else " "
            res += "  "
        res += "\n"

    res += "    -"
    res += "-" * (len(categories) * 3)

    for i in range(0, len(max(names, key=len))):
        res += "\n"
        res += "     "
        for name in names:
            res += name[i] if i < len(name) else " "
            res += "  "

    return res