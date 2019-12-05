# from __future__ import print_function
# import datetime
# import pickle
# import os.path
# import requests
# import json
# import time
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

from gcalendar import GCalendar
from magicseaweed import MagicSeaweedLocation, MagicSeaweedReport
from metoffice import MetOfficeLocation
from tide import Tide


def stash_json(self, data, filename):
    with open(filename, "w") as fp:
        json.dump(data, fp, indent=2)

def load_json(self, filename):
    with open(filename, "r") as fp:
        data = json.load(fp)
    return data



def main():
    gc = GCalendar("./config")
    gc.delete_all_events()
    
    events = []

    MAGICSEAWEED = load_json("./config/magicseaweed-config.json")
    TIDE = load_json("./config/tide-config.json")
    METOFFICE = load_json("./config/metoffice-config.json")
    
    msspot = MAGICSEAWEED["locations"][0]
    mskey = MAGICSEAWEED["key"]
    events.extend(MagicSeaweedLocation(msspot["name"], msspot["id"], mskey).get_events())
    
    tidespot = TIDE["locations"][0]
    tidekey = TIDE["key"]
    events.extend(Tide(tidespot["name"], tidespot["id"], tidekey).get_events())


    metspot = METOFFICE["locations"][0]
    metid = METOFFICE["metid"]
    metsecret = METOFFICE["metsecret"]
    events.extend(MetOfficeLocation(
        location = metspot["name"],
        _long = metspot["_long"],
        lat = metspot["lat"],
        metid = metid,
        metsecret = metsecret
    ).get_events())


    for event in events:
        gc.create_event(event)

if __name__ == "__main__":
    main()
