from pymongo import MongoClient
from twilio.rest import Client as TwilioClient

with open('.key','r') as f:
    lines = f.readlines()
    mongoURL = lines[1].strip()
    mongoUSER = lines[2].strip()
    mongoPASS = lines[3].strip()

print(mongoURL, mongoUSER, mongoPASS)

def get_db_handle():
    client = MongoClient(mongoURL, username=mongoUSER, password=mongoPASS)
    return client