from pykml import parser
from os import path

# Specify the namespace used in your KML file
ns = {'ns': 'http://www.opengis.net/kml/2.2'}

lat_list = []
lon_list = []

# Parse the KML file and get the root element
with open('PH 2023 Latest.kml') as f:
    root = parser.parse(f).getroot()

# Loop through all Placemark elements and extract the coordinates
for pm in root.xpath('//ns:Placemark', namespaces=ns):
    name = pm.name.text
    coords = pm.Point.coordinates.text.strip().split(',')
    longitude, latitude, altitude = [float(c) for c in coords]
    lat_list.append(latitude)
    lon_list.append(longitude)

    print(name, coords)

# # Parse the KML file
# with open('PH 2023 Latest.kml', 'rt') as kml_file:
#     kml_data = kml_file.read().encode('utf-8')
#     kml = parser.fromstring(kml_data)

# # Extract coordinates from markers
# coordinates = []
# for pm in kml.Document.Placemark:
#     # Check if the placemark has a Point geometry
#     if hasattr(pm.geometry, 'Point'):
#         # Extract the coordinates from the Point geometry
#         coords = pm.geometry.Point.coordinates.text.strip()
#         lon, lat, alt = coords.split(',')
#         coordinates.append((float(lon), float(lat)))

# # Print the extracted coordinates
# print(coordinates)
