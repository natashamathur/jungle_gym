import json
import ast
import argparse
from datetime import datetime

# should be run locally

categories = ["rent", "travel", "transit", "gym", "donations", "food", "discretionary"]
valid_actions = ["add", "set budget", "report card", "breakdown", "options"]
blank_expenses = """{'rent': {'budget': 0, 'spent': 0, 'items': {}},
                'travel': {'budget': 0, 'spent': 0, 'items': {}},
                'transit': {'budget': 0, 'spent': 0, 'items': {}},
                'gym': {'budget': 0, 'spent': 0, 'items': {}},
                'donations': {'budget': 0, 'spent': 0, 'items': {}},
                'food': {'budget': 0, 'spent': 0, 'items': {}},
                'discretionary': {'budget': 0, 'spent': 0, 'items': {}}}"""


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
    if budget_or_spent == "both":
        ledger = ast.literal_eval(blank_expenses)
    else:
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
            report = round(
                (ledger[category]["spent"] / ledger[category]["budget"]) * 100
            )
            if report >= 80:
                print("EIGHTY PERCENT USED")
            if report >= 100:
                print("NO MORE BUDGET FOR {}".format(category))
            total_spent += ledger[category]["spent"]
            print(
                "{}: {}% (${})".format(
                    category.title(),
                    str(report),
                    "{:.2f}".format(ledger[category]["spent"]),
                )
            )

    print()
    print("Total Spent: ${:.2f}".format(total_spent))

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


def display_options(categories=categories, actions=valid_actions):
    print("The possible actions are: {}".format(", ".join(actions)))
    print("The default categories are: {}".format(", ".join(categories)))
