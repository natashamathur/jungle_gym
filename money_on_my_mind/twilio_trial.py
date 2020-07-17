import os
from flask import Flask, request
from twilio import twiml
from twilio.rest import Client

# requirements: flask, twilio


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = os.environ["TWILIO_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


app = Flask(__name__)


def send_message(body, to, from_="+12039039945"):
    message = client.messages.create(body=body, from_=from_, to=to)


send_message("Welcome to your budget tracker", to="+19144822568")


@app.route("/sms", methods=["GET", "POST"])
def incoming_sms():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    body = request.values.get("Body", None)

    # Add a message
    resp = MessagingResponse()

    if body == "hello":
        resp.message("hi!")
    else:
        resp.message("whaddya mean")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
