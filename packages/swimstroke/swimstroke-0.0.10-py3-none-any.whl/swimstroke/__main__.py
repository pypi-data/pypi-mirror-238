import sys
from .helpers import load, get_events, populate_heats
from .util import swimtimefmt

for filename in sys.argv[1:]:
    print(filename)
    meetinfo = load(filename)
    #print(repr(meetinfo.))

    for event in get_events(meetinfo):
        populate_heats(event)
        print(event['event_number'],event['gender'],event['stroke'],event['distance'],event['course'],event['date'])
        for elinfo in event['eligibility']:
            print(" * ",elinfo['gender'],elinfo['age_from'],"-",elinfo['age_to'],elinfo['course'],swimtimefmt(elinfo['time_ms']))
        for entry in event['entries']:
            #print(repr(entry))
            if entry['relay']:
                print(" * relay - ",entry['heat'],entry['lane'],entry['teamname'],', '.join([e['name'] for e in entry['swimmers']]),entry['event_type'])
            else:
                print(" * ",entry['heat'],entry['lane'],entry['swimmers'][0]['name'],swimtimefmt(entry['seed_time_ms']),entry['event_type'])

