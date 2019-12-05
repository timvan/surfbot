import requests
import json
import datetime

class MetOfficeLocation(object):

    def __init__(self, location, _long, lat, metid, metsecret):
        self.location = location
        self.long = _long
        self.lat = lat
        self.metid = metid
        self.metsecret = metsecret
        self.minwindspeed = 15
    
    def get_report(self):
        frequency = "hourly"
        base = "https://api-metoffice.apiconnect.ibmcloud.com/metoffice/production/v0/forecasts/point/"
        query = f"{frequency}?latitude={self.lat}&longitude={self.long}"

        url = base + query

        headers = {
            "accept": "application/json",
            "x-ibm-client-id": self.metid,
            "x-ibm-client-secret": self.metsecret
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception("Request error {}".format(response.status_code))

        return response.json()

    def get_events(self):
        
        report = self.get_report()
        data = report["features"][0]["properties"]["timeSeries"]

        events = []

        for d in data:
            if self.is_windy(d):
                events.append(self.to_event(d))

        return events

    def is_windy(self, data):

        windgustspeed = int(data["windGustSpeed10m"]) if "windGustSpeed10m" in data else None

        if windgustspeed >= self.minwindspeed:
            return True

    def to_event(self, data):

        start = datetime.datetime.fromisoformat(data["time"][0:-1])
        end = start + datetime.timedelta(hours=1)


        windgustspeed = int(data["windGustSpeed10m"]) if "windGustSpeed10m" in data else None
        maxgustspeed = int(data["max10mWindGust"]) if "max10mWindGust" in data else None

        winddirection = self.degrees_to_direction(data["windDirectionFrom10m"])

        return {
            'summary': f'{windgustspeed}mph | {maxgustspeed}mph | {winddirection}',
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

    def degrees_to_direction(self, degrees):

        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE" "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        arc = 360 / len(directions)
        shifted_degrees = (degrees + arc / 2) % 360

        for i, d in enumerate(directions):
    
            if degrees >= i * arc and degrees <= (1 + i) * arc:
                return d


if __name__ == "__main__":
    
    mo = MetOfficeLocation(
        location = "Weston-Super-Mere",
        _long = "51.327538",
        lat = "-2.987934",
        metid = "60694de3-b2e1-49a9-bfc8-31dd8827b725",
        metsecret = "jX6uQ6sU1bV6lL0qH0pK6fQ5kG5kE0eW3mB7xX1gV3yX4pY0lM"
    )

    events = mo.get_events()

    
    
    print(json.dumps(events, indent=2))