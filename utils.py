from pymongo import MongoClient
from twilio.rest import Client as TwilioClient

with open('.key','r') as f:
    lines = f.readlines()
    mongoURL = lines[1]
    mongoUSER = lines[2]
    mongoPASS = lines[3]

def get_db_handle():
    client = MongoClient(mongoURL, username=mongoUSER, password=mongoPASS)
    return client