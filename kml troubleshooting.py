with open('PH 2023 Latest.kml') as f:
    root = parser.parse(f).getroot()

for pm in root.xpath('//ns:Placemark', namespaces=ns):
    name = pm.name.text
    coords = pm.Point.coordinates.text.strip().split(',')
    longitude, latitude, altitude = [float(c) for c in coords]
    lat_list.append(latitude)
    lon_list.append(longitude)
    names.append(name)

for i in range(len(names)):

    if names[i] in pole_ids:
        match_names.append((names[i],lat_list[i],lon_list[i]))

for i in range(len(match_names)):
    if match_names[i][0] in pole_ids:
        if match_names[i][0] in matches:
            matches[match_names[i][0]].append((match_names[i][1], match_names[i][2]))
        else:
            matches[match_names[i][0]] = [(match_names[i][1], match_names[i][2])]
####################### END Match KML Pole Names with Pole IDs #######################
