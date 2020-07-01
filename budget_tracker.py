import json
import ast
import argparse

# should be run locally

categories = ["rent", "travel", "transit", "gym", "donations", "food", "discretionary"]
blank_expenses = "{'rent': {'budget': 0, 'spent': 0, 'items': []}, 'travel': {'budget': 0, 'spent': 0, 'items': []}, 'transit': {'budget': 0, 'spent': 0, 'items': []}, 'gym': {'budget': 0, 'spent': 0, 'items': []}, 'donations': {'budget': 0, 'spent': 0, 'items': []}, 'food': {'budget': 0, 'spent': 0, 'items': []}, 'discretionary': {'budget': 0, 'spent': 0, 'items': []}}"


def open_ledger(filename="expenses.json"):

    with open(filename, "r") as fp:
        ledger = json.load(fp)
    return ledger


def close_ledger(ledger, filename="expenses.json"):
    with open(filename, "w") as fp:
        json.dump(ledger, fp)


def reset_all(ledger, budget_or_spent):
    # type should be "budget" or "spent"
    for category in ledger.keys():
        ledger[category][budget_or_spent] = 0


def set_budget(ledger, category, amount):
    ledger[category]["budget"] = amount
    return ledger


def add_expense(ledger, category, amount, item):
    ledger[category]["spent"] = ledger[category]["spent"] + amount
    ledger[category]["breakdown"][item] = amount
    return ledger


def report_card(ledger):
    print()
    print("MONTH TO DATE")
    print()
    total_spent = 0
    for category in ledger.keys():
        if ledger[category]["spent"] > 0:
            report = ledger[category]["spent"] / ledger[category]["budget"]
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
    print("Total Spent: {}".format(total_spent))


def action_add_purchase():
    ledger = open_ledger(fn)

    category, amount, item = args.d.split(" ")
    category, amount, item = category.strip(" "), float(amount), item.strip(" ")
    ledger = add_expense(ledger, category, amount, item)
    report_card(ledger)

    close_ledger(ledger, fn)


def action_set_budget():
    ledger = open_ledger(fn)

    category, amount = args.d.split(" ")
    category, amount = category.strip(" "), float(amount)
    ledger = set_budget(ledger, category, amount)

    close_ledger(ledger, fn)


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

        action_add_purchase()

    if args.action == "set budget":
        if not args.d or len(args.d.split(" ")) < 2:
            print("""Please enter values in the form "gym 80" """)
            quit()

        action_set_budget()

    if args.action == "report card":
        ledger = open_ledger(fn)
        report_card(ledger)
        close_ledger(ledger, fn)

    if args.action == "budget item":
        ledger = open_ledger(fn)
        category = ledger[args.d]
        print("Budget: {}".format(category["budget"]))
        print("Spent: {}".format(category["spent"]))
        print("On: {}".format(category["breakdown"]))
        close_ledger(ledger, fn)
