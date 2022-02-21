class Category:
    description = ""
    def __init__(self, category):
        self.ledger = list()
        self.category = category
        self.balance = 0.00

    def deposit(self, amount, description = ""):
        self.ledger.append({"amount": amount, "description": description})
        self.balance = self.balance + amount

    def get_balance(self):
        balance = 0.00
        for item in self.ledger:
            balance += item["amount"]
        return balance


    def check_funds(self, amount):
        if self.get_balance() >= amount:
            return True
        else:
            return False

    def withdraw(self, amount, description = ""):
        if self.check_funds(amount):
            self.balance = self.balance - amount
            self.ledger.append({"amount": -1 * amount, "description": description})
            return True
        else:
            return False

    def transfer(self, amount, to_category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + to_category.category)
            to_category.deposit(amount, "Transfer from " + self.category)
            return True
        else:
            return False

    def __str__(self):
        header = ""
        body = ""
        bottom = ""
        header = self.category.center(30, '*')
        # get description & amount from ledger list
        for item in self.ledger:
            body += f'{item["description"][:23]:23}' + f'{item["amount"]:>7.2f}' + '\n'
        total = f"{self.balance:.2f}"
        bottom = "Total: " + total
        output = header + "\n" + body + bottom
        return output

def create_spend_chart(categories):
    #find total spent & spent percent of each category
    total_spent = list() # total spent in each category
    category_name = list()
    for category in categories:
        category_name.append(category.ledger)
        spent = 0
        for action in category.ledger:
            if action["amount"] < 0:
                spent += (action["amount"] * -1)
        total_spent.append(spent)
    total = sum(total_spent)
    percent_list = list() # find percent spent in each category
    for expend in total_spent:
        percent_spent = (expend * 100) / total
        percent_list.append(percent_spent)
    #assemble
    title = "Percentage spent by category" + "\n"
    graph_width = len(category_name) * 3 + 5
    y = ""
    for num in range(100, -10, -10): # from 100 to -10, count down every -10
        y += str(num).rjust(3) + "|" # set y-axis
        #print(y)
        for percent in percent_list:
            if percent >= num:
                y += " o "
            else:
                y += " " * 3
        y += " \n"
    y = title + y
    dash = " " * 4 + "-".rjust(graph_width - 4, "-")
    y = y + dash
    #print(y)

    label = ""
    #fine the longest name, length of the name = times to iterate through the loop
    height = 0
    for name in categories:
        if len(name.category) > height:
            height = len(name.category)
    for index in range(height):
        label += "\n" + " " * 4
        for name in categories:
            if index < len(name.category):
                label += name.category[index].center(3, " ")
            else:
                label += " " * 3
        label = label + " "
    y = y + label
    return y


#food = budget.Category("Food")
food = Category('Food')
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)
food.deposit(900, "deposit")
food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
entertainment = Category("Entertainment")
food.transfer(20, entertainment)


print(food)
print(clothing)
print(auto)
print(entertainment)


print(create_spend_chart([food, clothing, auto]))
