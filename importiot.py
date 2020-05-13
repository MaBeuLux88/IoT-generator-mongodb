#!/usr/bin/env python3
# call with parameter: MongoDB URI.

import datetime
import random
import statistics
import sys
from _datetime import timedelta

from pymongo import MongoClient, WriteConcern

# constants
device_list = ["PTA101", "PTA299", "BRA001", "FRZ191", "FRB980", "AUS009", "JPY891", "JPY791", "ITI112", "SPL556"]
start_date = datetime.datetime(2020, 1, 1)  # first day to inject data
days = 100  # number of days to inject


# Returns a new temperature using delta and min/max values
def change_temp(temp, mini, maxi, delta):
    variation = random.randint(0, delta) - (delta / 2)
    if (temp + variation > maxi) or (temp + variation < mini):
        return temp - variation
    else:
        return temp + variation


def run(coll, device):
    docs = []

    for j in range(days):
        current_date = start_date + timedelta(days=j)
        temp = random.randint(17, 23)
        for _ in range(24):
            missed = random.randint(0, 3)  # simulates missing measures

            values = []
            temperatures_list = []
            for i in range(60 - missed):
                values.append({"measureMinute": i, "measuredValue": round(float(temp), 2)})
                temperatures_list.append(temp)
                temp = change_temp(temp, 13, 29, 5)

            docs.append({
                "id": device,
                "measureDate": current_date + timedelta(hours=i),
                "measureUnit": "°C",
                "periodAvg": round(statistics.mean(temperatures_list), 2),
                "periodMax": round(float(max(temperatures_list)), 2),
                "periodMin": round(float(min(temperatures_list)), 2),
                "missedMeasures": missed,
                "recordedMeasures": 60 - missed,
                "values": values
            })
    print('Inserting', len(docs), 'docs for device:', device)
    coll.insert_many(docs)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("You forgot the MongoDB URI parameter!")
        print(" - example: mongodb://mongo1,mongo2,mongo3/test?replicaSet=replicaTest&retryWrites=true")
        print(" - example: mongodb+srv://user:password@cluster0-abcde.mongodb.net/test?retryWrites=true")
        exit(1)
    mongo = MongoClient(host=(sys.argv[1]), socketTimeoutMS=10000, connectTimeoutMS=10000, serverSelectionTimeoutMS=10000)
    world = mongo.get_database("world")
    iot = world.get_collection("iot", write_concern=WriteConcern(w=1, wtimeout=8000))
    iot.drop()

    for d in device_list:
        run(iot, d)
