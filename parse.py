import json
import difflib
countries = {}
iso = {}
not_found = []
hardcoded_map = {"Republic of Moldova":"Moldova, Republic of",
                 "United Kingdom of Great Britain and Northern Ireland":"United Kingdom",
                 "The former Yugoslav Republic of Macedonia": "Macedonia",
                 "Democratic Republic of the Congo": "Congo, the Democratic Republic of the",
                 "Gambia (Islamic Republic of the)":"Gambia",}

fillKeys = {'3':"WORST",'2':"BAD",'1':"BETTER",'0':"BEST"}

with open('world.hires.json') as data_file:    
    world = json.load(data_file)
    #import pdb; pdb.set_trace()
    for country in world[u'features']:
        if u'properties' in country:
            iso[country[u'properties'][u'name']] = country[u'properties'][u'iso']

    with open("countries.txt") as file:
        country = None
        for line in file.readlines():
            line = line[:-2]
            if "/" in line:
                if country is not None:
                    name = hardcoded_map.get(country['name'],country['name'])
                    if name in iso:
                        countries[str(iso[name])]=country
                        del(iso[name])

                    else:
                        not_found.append(country)
                country = None
                line = line.split("/")
                if len(line)>2:
                    if len(line[2])>0:
                        country = dict(name=line[0].strip(), fillKey=fillKeys.get(line[2][-1],'UNKNOWN'), history='')
            else:
                if len(line.strip())>1 and country is not None:
                    country['history']+=line+'<br />'

keys = iso.keys()
for country in not_found:
    name = difflib.get_close_matches(country['name'], keys)[0]
    countries[str(iso[name])]=country
    #print country['name']
    #print difflib.get_close_matches(country['name'], keys)
    del(iso[name])



print countries