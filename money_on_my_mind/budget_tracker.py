from functions_for_budget_tracker import *


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

    requested_action = find_closest(
        args.action.lower(), choices=valid_actions
    )  # account for misspellings
    print("Taking Action: {}".format(requested_action))
    if requested_action not in valid_actions:
        print("Invalid Category")
        display_options()

    if requested_action == "add":
        if not args.d or len(args.d.split(" ")) < 3:
            print("""Please enter values in the form "food 25 takeout" """)
            quit()

        add_record("spending", fn, args.d)

    if requested_action == "set budget":
        if not args.d or len(args.d.split(" ")) < 2:
            print("""Please enter values in the form "gym 80" """)
            quit()

        add_record("budget", fn, args.d)

    if requested_action == "report card":
        report_card(fn)

    if requested_action == "breakdown":
        if not args.d:
            print("Please enter the category you want broken down.")
        report_on_item(fn, args.d)

    if requested_action == "options":
        display_options()

    if requested_action == "reset":
        if args.d:
            to_erase = args.d
        else:
            to_erase = "spent"
        reset_all(fn, args.d)
