from pymongo import MongoClient
from twilio.rest import Client as TwilioClient

def get_db_handle():
    client = MongoClient('mongodb+srv://bookhawaii.eyhrv.mongodb.net/myFirstDatabase', username='Stair', password='4q0khheB27jVnY8m')
    return client


def send_text(num):
    account_sid = "AC9586ca6c4a1805ab6e432984b7c8647f"
    auth_token = "66974f604ef2934fe09d6c9b5c87f169"
    client = TwilioClient(account_sid, auth_token)

    message = client.messages.create(
        body="Hello, world",
        from_="+18339101888",
        to=num
    )

    print(message.sid)

if __name__ == '__main__':
    print('running')
    send_text('2566822445')