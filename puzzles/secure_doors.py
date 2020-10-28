# Source: https://uchicago.kattis.com/problems/securedoors
# Time: 25 mins

events = [
    "entry Abbey",
    "entry Abbey",
    "exit Abbey",
    "entry Tyrone",
    "exit Mason",
    "entry Demetra",
    "exit Latonya",
    "entry Idella",
]


def secure_doors(events):
    logger = {}
    final = ""
    choices = {"entry": "entered", "exit": "exited"}

    for event in events:
        anomaly = False
        event = event.split(" ")
        if event[1] in logger.keys() and logger[event[1]] == event[0]:
            anomaly = True
        if event[1] not in logger.keys() and event[0] == "exit":
            anomaly = True
        logger[event[1]] = event[0]
        output = event[1] + " " + choices[event[0]]
        if anomaly == True:
            output = output + " (ANOMALY) "
        final = final + output + "\n"
    return final


print(secure_doors(events))

"""
Output:

Abbey entered
Abbey entered (ANOMALY) 
Abbey exited
Tyrone entered
Mason exited (ANOMALY) 
Demetra entered
Latonya exited (ANOMALY) 
Idella entered

"""
