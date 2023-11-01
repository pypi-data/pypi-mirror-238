# load the CTS SCB scoreboard files to get event/heat/lane information with swimmer names and clubs
import re
from .hy3 import HY3_STROKE_CODES, HY3_STROKE_CODES_SHORT, HY3_EVENT_GENDER_CODES

def load(fileobjs):
    # get an array of file objects
    teams = {}
    swimmers_by_team_and_name = {}
    for scbfo in fileobjs:
        line = scbfo.readline().decode('latin')
        mobj = re.match(r"#(\d+)\s{1,3}(GIRLS|MIXED|BOYS|MEN|WOMEN|MENS|WOMENS)\s{1,3}(?:\S+\s{1,3})?(\d+)\s{1,3}((?:IM|MEDLEY|FLY|FREE|FREESTYLE|BACK|BACKSTROKE|BREAST|BREASTSTROKE)(?: RELAY)?)", line)
        if mobj is None:
            raise Exception("unknown line format", line)
        event_number = int(mobj.group(1),10) # can we assume this will always be a number? May need to update the regex above
        distance = int(mobj.group(3),10)
        gender_str = mobj.group(2)
        event_gendercode = None
        for gkey,gvalue in HY3_EVENT_GENDER_CODES.items():
            if gender_str.lower() == gvalue.lower():
                gender_str = gvalue # normalize gender code
                event_gendercode = gkey
                break
        
        stroke_str = mobj.group(4)
        strokecode = None
        for scode, stroke_value in HY3_STROKE_CODES_SHORT.items():
            if stroke_str.lower() == stroke_value.lower():
                strokecode = scode
                stroke_str = stroke_value
                pass
        for scode, stroke_value in HY3_STROKE_CODES.items():
            if stroke_str.lower() == stroke_value.lower():
                strokecode = scode
                stroke_str = stroke_value
                pass
        
        #print("event_number",event_number,"distance",distance,"stroke",mobj.group(4),"gender",mobj.group(2))
        heat = 0
        while heat is not None:
            heat += 1
            for lane in range(1,11): # always 10 lanes of data
                line = scbfo.readline().decode('latin')
                if not line:
                    heat = None
                    break
                name = line[0:20].strip()
                team = line[22:].strip()
                if len(name)==0: continue # no one here
                #print("found",name,"team",team,"in lane",lane)
                if team not in teams:
                    teams[team] = {"short_name":team,"name":team,"entries":[],"swimmers":[]}
                if (team,name) not in swimmers_by_team_and_name:
                    cur_swimmer = {"name":name,
                        "lastname":name,"firstname":name,
                        "swimmer_code":hash(name),
                        "middlei":None,
                        "birthday_str":None,
                        "age":None,
                        "team_short_name":team,
                        "preferredname":name}
                    swimmers_by_team_and_name[(team,name)] = cur_swimmer
                    teams[team]['swimmers'].append(cur_swimmer)
                else:
                    cur_swimmer = swimmers_by_team_and_name[(team,name)]
                entry = {
                    "event":event_number,
                    "event_str":mobj.group(1),
                    "event_gendercode":event_gendercode,
                    "event_gender":gender_str,
                    "event_course":None,
                    "event_coursecode":None,
                    "event_type":"Final",
                    "heat":str(heat),
                    "heat_number":heat,
                    "lane":lane,
                    "stroke":HY3_STROKE_CODES[strokecode],
                    "strokeshort":HY3_STROKE_CODES_SHORT[strokecode],
                    "distance":distance,
                    "seed_time":None,
                    "seed_course":None,
                    "seed_coursecode":None,
                    "seed_time_ms":None,
                    "seed_time_str":"",
                    "swimmer_codes":[cur_swimmer['swimmer_code']],
                    "relay":False,
                }
                teams[team]['entries'].append(entry)
    teams = [value for _,value in teams.items()] # convert to array
    return {
        "teams":teams,
        "name":None,
        "location":None,
        "startdate":None,
        "enddate":None,
    }