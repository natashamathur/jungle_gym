# Money On My Mind

An expense tracker that provides a way to enter in expenses and continually compare to a provided budget. 
For most functionality, must be run from the command line with an individual budget saved as a json locally. 

Status updates can be obtained via a text message to Twilio. 

_TO DO: Add more functionality via Twilio_

## Packages: 
Default: `json`, `ast`, `argparse`, `datetime`

Additional: [`nltk`](https://www.nltk.org/install.html)

### For Use With Messaging:
- [ngrok](https://dashboard.ngrok.com/get-started/setup)
- [Twilio](https://www.twilio.com/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)

## Files
- [`cl_budget_tracker.py`](https://github.com/natashamathur/jungle_gym/blob/master/money_on_my_mind/cl_budget_tracker.py) Main run file from command line
- [`functions_for_budget_tracker.py`](https://github.com/natashamathur/jungle_gym/blob/master/money_on_my_mind/functions_for_budget_tracker.py) Helper functions
