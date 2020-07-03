import json
import ast
import argparse
from datetime import datetime

# should be run locally

categories = ["rent", "travel", "transit", "gym", "donations", "food", "discretionary"]
blank_expenses = "{'rent': {'budget': 0, 'spent': 0, 'items': []}, 'travel': {'budget': 0, 'spent': 0, 'items': []}, 'transit': {'budget': 0, 'spent': 0, 'items': []}, 'gym': {'budget': 0, 'spent': 0, 'items': []}, 'donations': {'budget': 0, 'spent': 0, 'items': []}, 'food': {'budget': 0, 'spent': 0, 'items': []}, 'discretionary': {'budget': 0, 'spent': 0, 'items': []}}"


def manage_ledger(action, ledger=None, filename="expenses.json"):
    # Load and save JSON file containing saved ledger

    if action == "open":
        with open(filename, "r") as fp:
            ledger = json.load(fp)
        return ledger

    if action == "close":
        with open(filename, "w") as fp:
            json.dump(ledger, fp)


def reset_all(filename, budget_or_spent):
    # type should be "budget" or "spent"
    ledger = manage_ledger("open", filename=fn)
    for category in ledger.keys():
        ledger[category][budget_or_spent] = 0
    manage_ledger("close", ledger=ledger)


def enter_item(action, ledger, details):
    # Enter a spending or saving amount

    
    if action == "spending":

        
        category, amount, item = details.split(" ")
        category, amount, item = category.strip(" "), float(amount), item.strip(" ")
        focus = ledger[category]
        
        focus["spent"] = focus["spent"] + amount
        if item not in focus["breakdown"].keys():
            focus["breakdown"][item] = amount
        else:
            focus["breakdown"][item] = focus["breakdown"][item] + amount
        return ledger

    if action == "budget":

        
        category, amount = details.split(" ")
        category, amount = category.strip(" "), float(amount)
        focus = ledger[category]
        
        focus["budget"] = amount
        return ledger


def report_card(filename):
    # Print out spending by category

    ledger = manage_ledger("open", filename=fn)

    print()
    print("MONTH TO DATE: {}".format(datetime.now().strftime("%B")))
    print()
    total_spent = 0
    for category in ledger.keys():
        if ledger[category]["spent"] > 0:
            report = ledger[category]["spent"] / ledger[category]["budget"]
            if report >= 0.8:
                print("EIGHTY PERCENT USED")
            if report >= 1:
                print("NO MORE BUDGET FOR {}".format(category))
            report = "{:.2f}".format(report)
            total_spent += ledger[category]["spent"]
            print(
                "{}: {}% (${})".format(
                    category.title(),
                    str(report),
                    "{:.2f}".format(ledger[category]["spent"]),
                )
            )

    print()
    print("Total Spent: ${}".format(total_spent))

    manage_ledger("close", ledger=ledger, filename=fn)



def add_record(action, fn, details):
    # Open ledger, enter item, close ledger
    ledger = manage_ledger("open", filename=fn)
    ledger = enter_item(action, ledger, details)
    manage_ledger("close", ledger=ledger)

    if action == "spending":
        report_card(ledger)

def report_on_item(filename, category):
    ledger = manage_ledger("open", filename=fn)
    category = ledger[category]
    print("Budget: {}".format(category["budget"]))
    print("Spent: {}".format(category["spent"]))
    print("On: {}".format(category["breakdown"]))
    manage_ledger("close", ledger=ledger)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action")
    parser.add_argument("--filename")
    parser.add_argument("--d")
    args = parser.parse_args()

    if args.filename:
        fn = args.filename
    else:
        fn = "expenses.json"

    if args.action == "add":
        if not args.d or len(args.d.split(" ")) < 3:
            print("""Please enter values in the form "food 25 "takeout" """)
            quit()

        add_record("spending", fn, args.d)

    if args.action == "set budget":
        if not args.d or len(args.d.split(" ")) < 2:
            print("""Please enter values in the form "gym 80" """)
            quit()

        add_record("budget", fn, args.d)

    if args.action == "report card":
        report_card(fn)

    if args.action == "breakdown":
        if not args.d:
            print("Please enter the category you want broken down.")
        report_on_item(fn, args.d)

    if args.action == "options":
        print(''' "add", "set budget", "report card", "breakdown" ''')
        print("Default Categories: {}".format(', '.join(categories)))
        
