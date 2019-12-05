from gcalendar import GCalendar
from magicseaweed import MagicSeaweedLocation, MagicSeaweedReport
from metoffice import MetOfficeLocation
from tide import Tide


def lambda_handler(event, context):
    gc = GCalendar()
    # gc.delete_all_events()
    
    events = []
    
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


    count = 0
    for event in events:
        # gc.create_event(event)
        count += 1

    return {
        'statusCode': 200,
        'body': f'Created {count} events'
    }
