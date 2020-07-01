import json
import ast
import argparse

categories = ['rent', 'travel', 'transit', 'gym', 'donations', 'food', 'discretionary']
blank_expenses = "{'rent': {'budget': 0, 'spent': 0, 'items': []}, 'travel': {'budget': 0, 'spent': 0, 'items': []}, 'transit': {'budget': 0, 'spent': 0, 'items': []}, 'gym': {'budget': 0, 'spent': 0, 'items': []}, 'donations': {'budget': 0, 'spent': 0, 'items': []}, 'food': {'budget': 0, 'spent': 0, 'items': []}, 'discretionary': {'budget': 0, 'spent': 0, 'items': []}}"


def open_ledger(filename='expenses.json'):
            
    with open(filename, 'r') as fp:
        ledger = json.load(fp)
    return ledger

def close_ledger(ledger, filename='expenses.json'):
    with open(filename, 'w') as fp:
        json.dump(ledger, fp)  

def reset_all(ledger, budget_or_spent):
    # type should be "budget" or "spent"
    for category in ledger.keys():
        ledger[category][budget_or_spent] = 0

def set_budget(ledger, category, amount):
    ledger[category]['budget'] = amount
    return ledger

def add_expense(ledger, category, amount, item):
    ledger[category]['spent'] = ledger[category]['spent'] + amount
    ledger[category]['items'].append(item)
    return ledger


def report_card(ledger):
    print("Month to Date:")
    print()
    total_spent = 0
    for category in ledger.keys():
        if ledger[category]['spent'] > 0:
            report = round(ledger[category]['spent'] / ledger[category]['budget'], 2)
            total_spent += ledger[category]['spent'] 
        else:
            report = 0
        print("{}: {}% (${})".format(category, str(report), ledger[category]['spent'], ))
    print()
    print("Total Spent: {}".format(total_spent))

def action_add_purchase():
    ledger = open_ledger(fn)
        
    category, amount, item = args.entry.split(" ")
    category, amount, item = category.strip(" "), float(amount), item.strip(" ")
    ledger = add_expense(ledger, category, amount, item)
    report_card(ledger)

    close_ledger(ledger, fn)

def action_set_budget():
    ledger = open_ledger(fn)
        
    category, amount = args.entry.split(" ")
    category, amount = category.strip(" "), float(amount)
    ledger = set_budget(ledger, category, amount)
    #print(ledger)
    #report_card(ledger)

    close_ledger(ledger, fn)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action')
    parser.add_argument('--filename')
    parser.add_argument('--entry')
    args = parser.parse_args()

    if args.action == 'test_read_in':
        e = ledger("open")
        print(e)

    if args.filename:
        fn = args.filename
    else:
        fn = 'expenses.json'

    if args.action == 'add':
        if not args.entry or len(args.entry.split(" ")) < 3:
            print('''Please enter values in the form "food, 25, "takeout" ''')
            quit()
                   
        action_add_purchase()

    if args.action == 'set budget':
        if not args.entry or len(args.entry.split(" ")) < 2:
            print('''Please enter values in the form "gym, 80" ''')
            quit()
                 
        action_set_budget()

    if args.action == 'report card':
        ledger = open_ledger(fn)
        report_card(ledger)
        close_ledger(ledger, fn)

    if args.action == 'budget item':
        ledger = open_ledger(fn)
        category = ledger[args.entry]
        print("Budget: {}".format(category['budget']))
        print("Spent: {}".format(category['spent']))
        print("On: {}".format(category['items']))
        close_ledger(ledger, fn)
