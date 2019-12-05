import requests
import json
import datetime

class MagicSeaweedLocation(object):
   
    def __init__(self, location, spot_id, key):
        self.location = location
        self.spot_id = spot_id
        self.base = "http://magicseaweed.com/api/"
        self.key = key

    def get_events(self):

        reports = self.get_report()
        events = []

        for report in reports:

            msreport = MagicSeaweedReport(report, self.location, self.spot_id)
            if msreport.worth_surfing():
                events.append(msreport.to_event())

        return events

    def get_report(self):
 
        url = f"{self.base}/{self.key}/forecast/?spot_id={self.spot_id}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception("Request error {}".format(response.status_code))

        return response.json()

class MagicSeaweedReport(object):
    
    def __init__(self, report, location, spot_id):
        self.spot_id = spot_id
        self.report = report
        self.location = location
        self.solidRatingMinimum = 3
    
    def worth_surfing(self):
        if self.report["solidRating"] >= self.solidRatingMinimum:
            return True
        return False

    def to_event(self):
        e = self.report
        ratingstr = "*" * e["solidRating"] + "o" * e["fadedRating"]

        start = datetime.datetime.fromtimestamp(e["localTimestamp"])
        end = start + datetime.timedelta(hours=3)

        max_swell = e["swell"]["maxBreakingHeight"]
        min_swell = e["swell"]["minBreakingHeight"]

        url = f"https://magicseaweed.com/{self.location}-Surf-Report/{self.spot_id}/"

        event = {
            'summary': f'[SURF] {self.location} {min_swell}-{max_swell}ft {ratingstr}',
            'location': '',
            'description': f'{url}',
            'start': {
                'dateTime': datetime.datetime.isoformat(start),
                'timeZone': 'Europe/London',
            },
            'end': {
                'dateTime': datetime.datetime.isoformat(end),
                'timeZone': 'Europe/London',
            }
        }

        return event
