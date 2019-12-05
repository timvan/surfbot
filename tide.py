import requests
import datetime
import json

class Tide(object):
    
    def __init__(self, station_name, station_id, api_key):
        self.station_id = station_id
        self.station_name = station_name
        self.url = f"https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/{station_id}/TidalEvents"
        self.api_key = api_key

    def get_report(self):

        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key
        }
        
        response = requests.get(self.url, headers=headers)

        if response.status_code != 200:
            raise Exception("Request error {}".format(response.status_code))

        return response.json()

    def to_event(self, report):

        start_str = report["DateTime"][0:19]
        start = datetime.datetime.fromisoformat(start_str)
        end = start + datetime.timedelta(minutes=5)

        event = {
            'summary': f'[TIDE] {report["EventType"]}',
            'location': '',
            'description': '',
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

    def get_events(self):
        return [self.to_event(r) for r in self.get_report()]



if __name__ == "__main__":
    tide = Tide("0527", "weston", "f1c8becfa7f44624844d32c663f0b891")
    report = tide.get_report()
    print(json.dumps(tide.get_events(), indent=2))
