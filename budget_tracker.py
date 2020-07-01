income = 8333

expenses = {}
expenses['rent'] = {'budget':1850, 'spent': 0, 'items': []}
expenses['travel'] = {'budget':200, 'spent': 0, 'items': []}
expenses['transit'] = {'budget':25, 'spent': 0, 'items': []}
expenses['gym'] = {'budget':80, 'spent': 0, 'items': []}
expenses['donations'] = {'budget':0, 'spent': 0, 'items': []}
expenses['food'] = {'budget':400, 'spent': 0, 'items': []}
expenses['discretionary'] = {'budget':631, 'spent': 0, 'items': []}

def reset_all(budget_or_spent):
    # type should be "budget" or "spent"
    for category in expenses.keys():
        expenses[category][budget_or_spent] = 0


def add_expense(category, amount, item):
    expenses[category]['spent'] = expenses[category]['spent'] + amount
    expenses[category]['items'].append(item)

def report_card():
    for category in expenses.keys():
        if expenses[category]['spent'] > 0:
            report = round(expenses[category]['spent'] / expenses[category]['budget'], 1)
        else:
            report = 0
        print("{}: {}%".format(category, str(report)))
