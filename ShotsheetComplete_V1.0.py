from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge import service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import os
import sys
import exifread
from datetime import datetime as dT
import datetime
import PyPDF2
import pdfrw
import pdfminer
import csv
import time
import math
from PyPDF4.generic import NameObject
from PyPDF4 import PdfFileWriter, PdfFileReader
from fillpdf import fillpdfs
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from pykml import parser
from os import path

def dms_to_dd(dms):
    degrees = dms[0]
    minutes = dms[1]
    seconds = dms[2]
    dd = degrees + minutes/60 + seconds/3600
    return dd

def fraction_to_float(fraction):
    """Converts a fraction to a floating-point number."""
    return float(fraction.num / fraction.den)

def save_credentials():
    # Get the values entered by the user
    username = username_var.get()
    pilot = pilot_var.get()
    team = team_var.get()

    with open('credentials.txt', 'w') as f:
        f.write(username + ',' + pilot + ',' + team)

    window.destroy()

def save_credentials():
    # Get the values entered by the user
    username = username_var.get()
    password = password_entry.get()
    pilot = pilot_var.get()
    team = team_var.get()
    print("Collection date:", folder_date)

    with open('credentials.txt', 'w') as f:
        f.write(username + ',' + password + ',' + pilot + ',' + team)

    window.destroy()

user_dir = os.path.expanduser("~")
desktop_dir = os.path.join(user_dir, "Desktop")
folder_date = ''
date_obj = ''
calendar_date = ''

def select_date(date_button):
    global folder_date, date_obj, calendar_date
    selected_date = str(date_label.selection_get())
    date_obj = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
    folder_date = '{:d}_{:d}_{:02d}'.format(date_obj.month, date_obj.day, date_obj.year % 100)
    date_obj = datetime.datetime.strptime(folder_date, '%m_%d_%y')
    calendar_date = date_obj.strftime('%B %#d, %Y')
    date_button.configure(text='Select Date\n(' + folder_date + ')')
    save_button.pack(pady=(30, 0))

date = datetime.datetime.now()
month = str(date.month)
day = str(date.day)
full_year = str(date.year)
year = str(date.year)[-2:]

if month.startswith('0'):
    month = month[1:]
if day.startswith('0'):
    day = day[1:]

today = f"{month}_{day}_{year}"

if os.path.isfile('credentials.txt'):
    # Read the credentials from the file
    with open('credentials.txt', 'r') as f:
        username, password, pilot, team = f.read().split(',')

    window = tk.Tk()
    window.title("Shotsheet Complete V1.0")
    window.geometry("500x700")

    # Add a label and dropdown menu for the user's name
    username_label = tk.Label(window, text="Field Maps Username/Password:")
    username_label.pack(pady=(5, 0))
    username_var = tk.StringVar(window)
    username_var.set(username) # default value
    username_menu = tk.OptionMenu(window, username_var, "mercury_precisionhawk", "venus_precisionhawk", "earth_precisionhawk", "mars_precisionhawk", "jupiter_precisionhawk", "saturn_precisionhawk", "neptune_precisionhawk")
    username_menu.pack(pady=(0,0)) # Add extra padding only at the bottom of the menu
    username_menu.config(width=25) # Set the width of the menu widget

    password_entry = tk.Entry(window, show='*')

    if username_var.get() == 'mars_precisionhawk' or username_var.get() =='earth_precisionhawk':
        password_entry.delete(0, tk.END)
        password_entry.insert(0, "Enter Password")
    else:
        password_entry.delete(0, tk.END)
        password_entry.insert(0, "Enter Password")

    password_entry.pack(pady=(0,25))

    # Add a label and dropdown menu for the user's name
    pilot_label = tk.Label(window, text="Pilot Name:")
    pilot_label.pack()
    pilot_var = tk.StringVar(window)
    pilot_var.set(pilot) # default value
    pilot_menu = tk.OptionMenu(window, pilot_var, "User 1", "User 2", "User 3", "User 4", "User 5", "User 6")
    pilot_menu.pack(pady=(0, 20))
    pilot_menu.config(width=25)

    # Add a label and dropdown menu for the user's name
    team_label = tk.Label(window, text="Team Name:")
    team_label.pack()
    team_var = tk.StringVar(window)
    team_var.set(team) # default value
    team_menu = tk.OptionMenu(window, team_var, "Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot")
    team_menu.pack(pady=(0, 30)) # Add extra padding only at the bottom of the menu
    team_menu.config(width=25) # Set the width of the menu widget

    date_label = Calendar(window, selectmode="day", year=int(full_year), month=int(month), day=int(day))
    date_label.pack(pady=(0,10))
    date_button = tk.Button(window, text="Select Collection Date", command=lambda: select_date(date_button), name="date_button")
    date_button.pack()

    warning_label = tk.Label(window, text="IMPORTANT\n(1) Create a folder on your desktop\n(2) Name the folder the selected date with format M_D_YY\n(3) Place all collected images from that day into the folder")
    warning_label.pack(pady=(10,0))

    # Add a button to save the credentials
    save_button = tk.Button(window, text="Run", command=save_credentials)
    save_button.config(width=10)
    save_button.pack_forget()

    # Display the window
    window.mainloop()

    # Read the credentials from the file
    with open('credentials.txt', 'r') as f:
        username, password, pilot, team = f.read().split(',')

    if pilot == "User 5":
        Pilot_ID_item = "expr_1.valueUnique_popup4"
    elif pilot == "User 3":
        Pilot_ID_item = "expr_1.valueUnique_popup1"
    elif pilot == "User 2":
        Pilot_ID_item = "expr_1.valueUnique_popup2"
    elif pilot == "User 1":
        Pilot_ID_item = "expr_1.valueUnique_popup3"
    elif pilot == "User 4":
        Pilot_ID_item = "expr_1.valueUnique_popup5"
    elif pilot == "User 6":
        Pilot_ID_item = "expr_1.valueUnique_popup0"

else:
    window = tk.Tk()
    window.title("Shotsheet Complete V1.0")
    window.geometry("500x700")

    username_label = tk.Label(window, text="Field Maps Username/Password:")
    username_label.pack(pady=(5, 0))
    username_var = tk.StringVar(window)
    username_var.set("Select Username") # default value
    username_menu = tk.OptionMenu(window, username_var, "mercury_precisionhawk", "venus_precisionhawk", "earth_precisionhawk", "mars_precisionhawk", "jupiter_precisionhawk", "saturn_precisionhawk", "neptune_precisionhawk")
    username_menu.pack(pady=(0, 20)) # Add extra padding only at the bottom of the menu
    username_menu.config(width=25) # Set the width of the menu widget

    password_entry = tk.Entry(window)

    if username_var.get() == 'mars_precisionhawk' or username_var.get() =='earth_precisionhawk':
        password_entry.delete(0, tk.END)
        password_entry.insert(0, "Enter Password")
        password_entry.update_idletasks()
    else:
        password_entry.delete(0, tk.END)
        password_entry.insert(0, "Enter Password")
        password_entry.update_idletasks()
    
    password_entry.pack(pady=(0,25))

    pilot_label = tk.Label(window, text="Pilot Name:")
    pilot_label.pack()
    pilot_var = tk.StringVar(window)
    pilot_var.set("Select Pilot") # default value
    pilot_menu = tk.OptionMenu(window, pilot_var, "User 1", "User 2", "User 3", "User 4", "User 5", "User 6")
    pilot_menu.pack(pady=(0, 20)) # Add extra padding only at the bottom of the menu
    pilot_menu.config(width=25) # Set the width of the menu widget

    team_label = tk.Label(window, text="Team Name:")
    team_label.pack()
    team_var = tk.StringVar(window)
    team_var.set("Select Team Name") # default value
    team_menu = tk.OptionMenu(window, team_var, "Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot")
    team_menu.pack(pady=(0, 30)) # Add extra padding only at the bottom of the menu
    team_menu.config(width=25) # Set the width of the menu widget

    date_label = Calendar(window, selectmode="day", year=int(full_year), month=int(month), day=int(day))
    date_label.pack(pady=(0,10))
    date_button = tk.Button(window, text="Select Collection Date", command=lambda: select_date(date_button), name="date_button")
    date_button.pack()

    warning_label = tk.Label(window, text="IMPORTANT\n(1) Create a folder on your desktop\n(2) Name the folder the selected date with format M_D_YY\n(3) Place all collected images from that day into the folder")
    warning_label.pack(pady=(10,0))

    # Add a button to save the credentials
    save_button = tk.Button(window, text="Run", command=save_credentials)
    save_button.config(width=10)
    save_button.pack_forget()

    # Display the window
    window.mainloop()

    # Read the credentials from the file
    with open('credentials.txt', 'r') as f:
        username, password, pilot, team = f.read().split(',')

     if pilot == "User 5":
        Pilot_ID_item = "expr_1.valueUnique_popup4"
    elif pilot == "User 3":
        Pilot_ID_item = "expr_1.valueUnique_popup1"
    elif pilot == "User 2":
        Pilot_ID_item = "expr_1.valueUnique_popup2"
    elif pilot == "User 1":
        Pilot_ID_item = "expr_1.valueUnique_popup3"
    elif pilot == "User 4":
        Pilot_ID_item = "expr_1.valueUnique_popup5"
    elif pilot == "User 6":
        Pilot_ID_item = "expr_1.valueUnique_popup0"

try:
    chrome_options = Options()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    browser = webdriver.Chrome(options=chrome_options)
except:
    edge_options = webdriver.EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument('headless')
    edge_options.add_argument('--disable-blink-features=AutomationControlled')
    browser = webdriver.Edge(options=edge_options)
print('\n' + 'Accessing Field Maps...' + '\n')

############################### Web Page Interface #################################
login_page = "https://precisionhawk.maps.arcgis.com/sharing/oauth2/authorize?client_id=arcgisWebApps&response_type=code&state=%7B%22portalUrl%22%3A%22https%3A%2F%2Fprecisionhawk.maps.arcgis.com%22%2C%22uid%22%3A%22AWKK7Vv0jjE1GmdAHdnCM3tQdaIrlfb3ertvchlAizA%22%7D&expiration=20160&locale=en-US&redirect_uri=https%3A%2F%2Fprecisionhawk.maps.arcgis.com%2Fapps%2Fmapviewer%2Findex.html%3Fwebmap%3Db13ac19c0f4848408cf0a214844f07cd&redirectToUserOrgUrl=true&code_challenge=h4jvrFEmwFIl67B5LrqjUXTxLvBs8LYyJ-rW8fvK5lM&code_challenge_method=S256"
browser.get(login_page)
wait = WebDriverWait(browser, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "user_username")))
username_field = browser.find_element(By.ID, "user_username")
password_field = browser.find_element(By.ID, "user_password")
username_field.send_keys(username)
password_field.send_keys(password)
password_field.submit()

classic_page = "https://precisionhawk.maps.arcgis.com/home/webmap/viewer.html?webmap=b13ac19c0f4848408cf0a214844f07cd"
browser.get(classic_page)
try:
    content_menu_button = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.ID, "webmap-details-legend-content")))
except TimeoutException:
    print("Login Error: Check Username/Password and make sure your internet connection is good.")
    while True:
        pass
content_menu_button.click()

print('\n' + 'Searching Structures...' + '\n')

span_filter_button = WebDriverWait(browser, 15).until(
    EC.presence_of_element_located((By.XPATH, "//span[@onclick=\"JavaScript:dijit.byId('tocPanel').filter('185f5f4d007-layer-1',null);\"]")))
span_filter_button.click()

filter1_dropdown = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.ID, "expr_1.fieldsList")))
filter1_dropdown.click()
time.sleep(1)
filter1_dropdown.send_keys(Keys.ARROW_DOWN)

pilot_menu_item = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.ID, "expr_1.fieldsList_popup13")))
pilot_menu_item.click()

unique_bubble = WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.XPATH, "//input[@title='Pick from unique values in selected field']")))
unique_bubble.click()

filter2_dropdown = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.ID, "expr_1.valueUnique")))
filter2_dropdown.click()
time.sleep(1)
filter2_dropdown.send_keys(Keys.ARROW_DOWN)

pilot_name_item = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, Pilot_ID_item)))
pilot_name_item.click()

add_expression_link = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Add another expression']")))
add_expression_link.click()

filter3_dropdown = WebDriverWait(browser, 10).until(
     EC.element_to_be_clickable((By.ID, "expr_2.fieldsList")))
filter3_dropdown.click()
time.sleep(1)
filter3_dropdown.send_keys(Keys.ARROW_DOWN)

coll_date_item = WebDriverWait(browser, 30).until(
    EC.element_to_be_clickable((By.ID, "expr_2.fieldsList_popup8")))
coll_date_item.click()

filter4_dropdown = WebDriverWait(browser, 30).until(
    EC.element_to_be_clickable((By.ID, "expr_2.value")))
filter4_dropdown.click()
time.sleep(1)
filter4_dropdown.send_keys(Keys.ARROW_DOWN)

print('\n' + 'Collecting IDs...' + '\n')

try:
    if date_obj.month < date.month:
        num_of_clicks = date.month - (date_obj.month)
        for i in range(num_of_clicks):
            calendar_back_arrow = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='dijitReset dijitCalendarArrow dijitCalendarDecrementArrow']")))
            calendar_back_arrow.click()
except AttributeError:
    print('AttributeError:\nPlease select a date')
    while True:
        pass

today_element = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, f'//td[@aria-label="{calendar_date}"]')))

today_element.click()
time.sleep(2.5)

apply_button = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "applyFilterAndZoomButton_label")))
WebDriverWait(browser, 30).until(
    lambda x: not apply_button.get_attribute("disabled"))
apply_button.click()

span_table_button = WebDriverWait(browser, 30).until(
    EC.element_to_be_clickable((By.XPATH, "//span[@onclick=\"JavaScript:dijit.byId('tocPanel').showAttributeTable('185f5f4d007-layer-1',null);\"]")))
span_table_button.click()

try:
    pole_id_elements = WebDriverWait(browser, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.field-structure div")))
except TimeoutException:
    print("Timed out waiting for structure IDs:\nMake sure the image folder is correctly named/dated\nFolder date must match collection date of structures in Field Maps")
    while True:
        pass

pole_ids = []
for element in pole_id_elements:
    attribute_value = element.get_attribute('innerHTML')
    pole_ids.append(attribute_value)
print('\n' + 'Extracting Data...' + '\n')
print(sorted(pole_ids),'\n')

parent_saps = []
parent_sap_elements = WebDriverWait(browser, 30).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.field-parent_sap div")))
for element in parent_sap_elements:
    attribute_value = element.get_attribute('innerHTML')
    parent_saps.append(attribute_value)
print(parent_saps,'\n')

structure_type_elements = WebDriverWait(browser, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.field-shotsheet div")))
structure_types = [e.text for e in structure_type_elements]
print(structure_types)
######################### For Future GPS Data on Field Maps #########################
# lattitude_elements = WebDriverWait(browser, 10).until(
#     EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.field-lattitude div")))
# lattitudes = [e.text for e in lattitude_elements]

# longitude_elements = WebDriverWait(browser, 10).until(
#     EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.field-longitude div")))
# longitudes = [e.text for e in longitude_elements]
#####################################################################################

############################# END Web Page Interface ################################
dt_obj = datetime.datetime.strptime(folder_date, '%m_%d_%y')
today_pdf = dt_obj.strftime('%#m/%#d/%y')

folder_path = f'{desktop_dir}/{folder_date}'      

# Get a list of all the files in the folder
try:
    files = os.listdir(folder_path)
except FileNotFoundError:
    print('\nFileNotFoundError:\nMake sure the folder: ' + folder_path + ' exists.')
    while True:
        pass
# Specify the namespace used in your KML file
ns = {'ns': 'http://www.opengis.net/kml/2.2'}

timestamps = []
lat_coordinates = []
lon_coordinates = []
lat_list = []
lon_list = []
names = []
match_names = []
matches = {}
photo_match = {}
index = 0 
print('\n' + 'Parsing KML...' + '\n')
####################### Match KML Pole Names with Pole IDs #######################
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

for file in files:
    file_path = os.path.join(folder_path, file)

    if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
        # Open the file and read the metadata
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)

        latitude = tags.get('GPS GPSLatitude')
        longitude = tags.get('GPS GPSLongitude')
        timestamp = str(tags.get('EXIF DateTimeOriginal'))
        iso_speed = tags.get('EXIF ISOSpeedRatings')

        # Add the timestamp to the list if it's the first file, or if the ISO speed is greater than 5000
        if len(timestamps) == 0 or (iso_speed is not None and int(iso_speed.values[0]) > 5000):
            timestamps.append(timestamp)

            # If this is not the first file and there is at least one more file, add the next timestamp to the list
            if len(timestamps) > 1 and index +1 < len(files):
                next_file_path = os.path.join(folder_path,files[index+1])

                with open(next_file_path, 'rb') as f_next:
                    tags_next = exifread.process_file(f_next)

                next_timestamp = str(tags_next.get('EXIF DateTimeOriginal'))
                timestamps.append(next_timestamp)

        prev_timestamp = timestamp
        index += 1

timestamps.sort()
index = 1
print('\n' + 'Matching Cordinates:' + '\n')
for pole_name, pole_coords in matches.items():
    closest_match = None
    min_distance = math.inf

    for coords in pole_coords:

        for file in files:
            file_path = os.path.join(folder_path, file)

            if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
                with open(file_path, 'rb') as f:
                    tags = exifread.process_file(f)

                latitude = tags.get('GPS GPSLatitude')
                longitude = tags.get('GPS GPSLongitude')
                timestamp = str(tags.get('EXIF DateTimeOriginal'))
                iso_speed = tags.get('EXIF ISOSpeedRatings')

                if latitude and longitude:
                            lat_dms = [fraction_to_float(d) for d in latitude.values]
                            long_dms = [fraction_to_float(d) for d in longitude.values]
                            lat_dd = dms_to_dd(lat_dms)
                            lon_dd = -1*dms_to_dd(long_dms)
                            # Calculate the Euclidean distance between the photo coordinates and the pole coordinates
                            distance = math.sqrt((coords[0] - lat_dd)**2 + (coords[1] - lon_dd)**2)
                            # Update the closest match if this distance is smaller than the current minimum
                            if distance < min_distance:
                                min_distance = distance
                                closest_match = file
                                closest_timestamp = timestamp

    photo_match[pole_name] = closest_timestamp
    print('Structure ', index, '...\n')
    index += 1

zip_poleid_saps = list(zip(pole_ids, parent_saps, structure_types))
photo_match_list = list(photo_match.items())
sorted_pole_timestamps = sorted(photo_match_list, key=lambda x: x[1])
pole_names, pole_timestamps = zip(*sorted_pole_timestamps)

try:
    zip_poleid_saps = sorted(zip_poleid_saps, key=lambda x: pole_timestamps[pole_names.index(x[0])])
except ValueError:
    print("Photo/Timestamp/Structure Match Error:\n-Make sure all images are present in folder\n-Structures are marked as collected\n-Only Inspected structures have coll_date\n-KML file is up to date.")
    import sys
    while True:
        pass

pole_ids, parent_saps, structure_types = zip(*zip_poleid_saps)
############################################# END JPG Extract Code #############################################
print('\n' + 'Exporting to PDF...' + '\n\n')
################################## Export to PDF #######################################
pdf_save_path1 = f'{desktop_dir}/Filled Shotsheets'
pdf_save_path2 = f'{pdf_save_path1}/{folder_date}'
if not os.path.exists(pdf_save_path1):
    os.mkdir(pdf_save_path1)
if not os.path.exists(pdf_save_path2):
    os.mkdir(pdf_save_path2)

start_flight = []
end_flight = []
formatted_sf = []
formatted_ef = []
PoleData_field = []

for i in range(0, len(timestamps), 2):
    start_flight.append(timestamps[i])
    sf = datetime.datetime.strptime(start_flight[-1], "%Y:%m:%d %H:%M:%S")
    formatted_sf.append(sf.strftime("%I:%M %p"))

    if i+1 < len(timestamps):
        end_flight.append(timestamps[i+1])
        ef = datetime.datetime.strptime(end_flight[-1], "%Y:%m:%d %H:%M:%S")
        formatted_ef.append(ef.strftime("%I:%M %p"))

Steel, Concrete, Wood, Fiberglass = 'Off', 'Off', 'Off', 'Off' 
try:
    for i in range(len(pole_ids)):
        PoleData = str(parent_saps[i]) + ' ' + str(pole_ids[i])
        PoleData_field.append(PoleData)

        if structure_types[i].lower() in ['tower','towr']:
            Tower = 'on'
            Steel = 'on'
            Concrete, Wood, Fiberglass = 'Off'
        else: 
            Tower = 'Off'

        if structure_types[i].lower() in ['frame', 'hframe']:
            Frame = 'on'
            Steel = 'on'
            Concrete, Wood, Fiberglass = 'Off'
        else: 
            Frame = 'Off'

        if structure_types[i].lower() in ['pole']:
            Pole = 'on'
            Wood = 'on'
            Steel, Concrete, Fiberglass = 'Off'
        else: 
            Pole = 'Off'

        if structure_types[i].lower() in ['multi', 'multi-structure', 'multistructure', 'multi structure']:
            Multi = 'on'
            Steel = 'on'
            Concrete, Wood, Fiberglass = 'Off'
        else: 
            Multi = 'Off'


        form_fields = fillpdfs.get_form_fields("PGE 2023.pdf")

        data_dict = {
        'dhFormfield-4055512778': 'Precision Hawk',
        'dhFormfield-4055513106': today_pdf,
        'dhFormfield-4055513200': team.upper(),
        'dhFormfield-4055516340': PoleData_field[i],
        'dhFormfield-4055516446': '', #Lat
        'dhFormfield-4055516466': '', #Long
        'dhFormfield-4055517287': formatted_sf[i],
        'dhFormfield-4055517747': formatted_ef[i], 
        'dhFormfield-4055517826': '', #Field Notes

        'dhFormfield-4055514808': Steel, #Steel
        'dhFormfield-4055520694': Concrete, #Concrete
        'dhFormfield-4055520764': Wood, #Wood
        'dhFormfield-4055520768': Fiberglass, #Fiberglass

        'dhFormfield-4055521364': Tower, #Tower
        'dhFormfield-4055522189': Frame, #H-Frame
        'dhFormfield-4055522223': Pole, #Pole
        'dhFormfield-4055522230': Multi, #Multi-Structure
        }

        pdf_save_dir = os.path.join(pdf_save_path2, parent_saps[i] + '.pdf')

        fillpdfs.write_fillable_pdf('PGE 2023.pdf', pdf_save_dir, data_dict)
except IndexError:
    print('IndexError:\nStructure count/timestamp mismatch. Make sure all images and white-out shots are present in folder\n')
    while True:
        pass

print('Pole ID' + '|' + '  SAP   ' + '|' + ' Start  ' + '|  End' + '\n')
for item, sf, ef in zip(PoleData_field, formatted_sf, formatted_ef):
    fields = item.split()
    new_item = fields[1] + ' ' + fields[0] + ' ' + sf + ' ' + ef
    print(new_item + '\n')
print('\n' + 'Shotsheet Complete! \n\nPDFs saved to Desktop/Filled Shotsheets/M_D_YY')
while True:
    pass
################################ END Export to PDF ##################################
