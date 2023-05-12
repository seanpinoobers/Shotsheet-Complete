from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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
from PyPDF4.generic import NameObject
from PyPDF4 import PdfFileWriter, PdfFileReader
from fillpdf import fillpdfs
import tkinter as tk
from tkinter import messagebox


# set up ChromeOptions to avoid detection
chrome_options = Options()
chrome_options.add_argument('headless') # Comment out if you want to watch the web page open and complete process
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
browser = webdriver.Chrome(options=chrome_options)

###################################################### Web Page Interface #############################################################
# Launch the Chrome browser and navigate to the login page
login_page = "https://precisionhawk.maps.arcgis.com/sharing/oauth2/authorize?client_id=arcgisWebApps&response_type=code&state=%7B%22portalUrl%22%3A%22https%3A%2F%2Fprecisionhawk.maps.arcgis.com%22%2C%22uid%22%3A%22AWKK7Vv0jjE1GmdAHdnCM3tQdaIrlfb3ertvchlAizA%22%7D&expiration=20160&locale=en-US&redirect_uri=https%3A%2F%2Fprecisionhawk.maps.arcgis.com%2Fapps%2Fmapviewer%2Findex.html%3Fwebmap%3Db13ac19c0f4848408cf0a214844f07cd&redirectToUserOrgUrl=true&code_challenge=h4jvrFEmwFIl67B5LrqjUXTxLvBs8LYyJ-rW8fvK5lM&code_challenge_method=S256"
browser.get(login_page)

# Wait for the login page to load
wait = WebDriverWait(browser, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "user_username")))

# Fill in the username and password fields
username_field = browser.find_element(By.ID, "user_username")
password_field = browser.find_element(By.ID, "user_password")
username_field.send_keys("mars_precisionhawk")
password_field.send_keys("pge2023!")

# Submit the login form
password_field.submit()

wait = WebDriverWait(browser, 15)
classic_page = "https://precisionhawk.maps.arcgis.com/home/webmap/viewer.html?webmap=b13ac19c0f4848408cf0a214844f07cd"
browser.get(classic_page)

# Find the content menu button element
content_menu_button = WebDriverWait(browser, 30).until(
    EC.presence_of_element_located((By.ID, "webmap-details-legend-content")))

# Click on the button
content_menu_button.click()

span_filter_button = WebDriverWait(browser, 15).until(
    EC.presence_of_element_located((By.XPATH, "//span[@onclick=\"JavaScript:dijit.byId('tocPanel').filter('185f5f4d007-layer-1',null);\"]")))

# Find the span element and click it

span_filter_button.click()

filter1_dropdown = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.ID, "expr_1.fieldsList")))

# click the dropdown menu
filter1_dropdown.click()

# add a small delay to give the dropdown menu time to load
time.sleep(0.5)

# send a down arrow key press to the dropdown menu to reveal the options
filter1_dropdown.send_keys(Keys.ARROW_DOWN)

# wait for the menu item to be clickable
pilot_menu_item = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.ID, "expr_1.fieldsList_popup13")))

# click the menu item to select it
pilot_menu_item.click()

# wait for the radio button to be clickable
unique_bubble = WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.XPATH, "//input[@title='Pick from unique values in selected field']")))

# click the radio button to select it
unique_bubble.click()

filter2_dropdown = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.ID, "expr_1.valueUnique")))

# click the dropdown menu
filter2_dropdown.click()

# add a small delay to give the dropdown menu time to load
time.sleep(0.5)

# send a down arrow key press to the dropdown menu to reveal the options
filter2_dropdown.send_keys(Keys.ARROW_DOWN)

# wait for the menu item to be clickable
pilot_name_item = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "expr_1.valueUnique_popup4")))

# click the menu item to select it
pilot_name_item.click()

add_expression_link = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Add another expression']")))

add_expression_link.click()

filter3_dropdown = WebDriverWait(browser, 10).until(
     EC.element_to_be_clickable((By.ID, "expr_2.fieldsList")))

# click the dropdown menu
filter3_dropdown.click()

# add a small delay to give the dropdown menu time to load
time.sleep(0.5)

# send a down arrow key press to the dropdown menu to reveal the options
filter3_dropdown.send_keys(Keys.ARROW_DOWN)

# wait for the menu item to be clickable
coll_date_item = WebDriverWait(browser, 30).until(
    EC.element_to_be_clickable((By.ID, "expr_2.fieldsList_popup8")))

# click the menu item to select it
coll_date_item.click()

filter4_dropdown = WebDriverWait(browser, 30).until(
    EC.element_to_be_clickable((By.ID, "expr_2.value")))

# click the dropdown menu
filter4_dropdown.click()

# add a small delay to give the dropdown menu time to load
time.sleep(1)

# send a down arrow key press to the dropdown menu to reveal the options
filter4_dropdown.send_keys(Keys.ARROW_DOWN)

today_date = f'{dT.today():%B %d, %Y}'.replace(' 0',' ')

# Find today's date element and click on it
today_element = WebDriverWait(browser, 30).until(
    EC.element_to_be_clickable((By.XPATH, f"//td[@aria-label='{today_date}']")))
# # ################################## Run a Previous Date ######################################
# today_element = WebDriverWait(browser, 30).until(
#     EC.element_to_be_clickable((By.XPATH, f"//td[@aria-label='March 23, 2023']")))
# # #############################################################################################

today_element.click()

time.sleep(2.5)

# wait for the menu item to be clickable
apply_button = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "applyFilterAndZoomButton_label")))

# wait for the button to become enabled
WebDriverWait(browser, 30).until(
    lambda x: not apply_button.get_attribute("disabled"))

# click the button
apply_button.click()

# open table
span_table_button = WebDriverWait(browser, 30).until(
    EC.element_to_be_clickable((By.XPATH, "//span[@onclick=\"JavaScript:dijit.byId('tocPanel').showAttributeTable('185f5f4d007-layer-1',null);\"]")))

span_table_button.click()

try:
    pole_id_elements = WebDriverWait(browser, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.field-structure div")))
except TimeoutException:
    print("Timed out waiting for pole ID elements, Check to make sure your poles are marked as collected for this day")
    import sys
    sys.exit(1)

# Extract text from pole ID elements
pole_ids = [e.text for e in pole_id_elements]

parent_sap_elements = WebDriverWait(browser, 30).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.field-parent_sap div")))

# Extract text from SAP elements
parent_saps = [e.text for e in parent_sap_elements]

structure_type_elements = WebDriverWait(browser, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.field-shotsheet div")))

# Extract text from structure elements
structure_types = [e.text for e in structure_type_elements]
###################################################### END Web Page Interface #########################################################

#################################### Sort Data ####################################
# # Combine the three lists into a list of tuples
# data = list(zip(parent_saps, pole_ids, structure_types))

# # Sort the list of tuples based on the pole_ids value
# sorted_data = sorted(data, key=lambda x: x[1])
# # sorted_data = sorted(data, key=lambda x: float(x[1].replace('/', '.')), reverse=True)

# # Prompt user for sorting order
# sort_order = input("Enter 'asc' for ascending or 'desc' for descending sorting: ")

# # Check user input and sort data accordingly
# if sort_order == 'asc':
#     sorted_data = sorted(data, key=lambda x: float(x[1].replace('/', '.')))
# elif sort_order == 'desc':
#     sorted_data = sorted(data, key=lambda x: float(x[1].replace('/', '.')), reverse=True)
# else:
#     print("Invalid input. Sorting in ascending order by default.")
#     sorted_data = sorted(data, key=lambda x: float(x[1].replace('/', '.')))

# # Print the sorted data
# for parent_sap, pole_id, structure_type in sorted_data:
    # print(f"SAP: {parent_sap}, ID: {pole_id}, Type: {structure_type}")

zip_lists = list(zip(pole_ids, parent_saps, structure_types))
sorted_lists = sorted(zip_lists, key=lambda x: x[0])
# sorted_lists = sorted_lists[::-1]

# Create a function to handle the Yes button click event
def handle_yes():
    messagebox.showinfo("ShotSheet AutoComplete V 1.0", "Poles sorted in ascending order!")

# Create a function to handle the No button click event
def handle_no():
    # Use the sorted_lists variable defined outside the function
    global sorted_lists
    sorted_lists = sorted_lists[::-1]
    messagebox.showinfo("ShotSheet AutoComplete V 1.0", "Poles sorted in descending order!")

result = messagebox.askquestion("ShotSheet AutoComplete V 1.0", "Were poles inspected in ascending numerical order?")

if result == 'yes':
    handle_yes()
else:
    handle_no()

# def get_input():
#     list_order = input()

#     while list_order.lower() not in ['y', 'yes', 'yep', 'ya', 'n', 'no']:
#         print('Invalid input. Please enter y or n.')
#         list_order = input()

#     if list_order.lower() in ['n', 'no']:
#         sorted_lists = sorted_lists[::-1]
#     else:
#         pass

# root = tk.Tk()

# label = tk.Label(root, text='\n Were poles inspected in ascending numerical order? \n (Example: You inspected pole 042/001, then 042/002, and then 042/003, etc.)\n \n Input y for (y)es and n for (n)o and then press ENTER \n \n')
# label.pack()

# entry = tk.Entry(root)
# entry.pack()

# button = tk.Button(root, text="Submit", command=get_input)
# button.pack()

# root.mainloop()

pole_ids, parent_saps, structure_types = zip(*sorted_lists)
################################## END Sort Data ##################################

############################################# JPG Extract Code #############################################
date = datetime.datetime.now()
month = str(date.month)
day = str(date.day)
year = str(date.year)[-2:]

if month.startswith('0'):
    month = month[1:]
if day.startswith('0'):
    day = day[1:]

today = f"{month}_{day}_{year}"
today_pdf = f"{month}/{day}/{year}"

# Define the path to the folder containing the photos
folder_path = f'C:/Users/Echo/Desktop/{today}'

# ############## Use Previous Day ###############
# folder_path = f'C:/Users/Echo/Desktop/3_23_23'
# ###############################################

# Get a list of all the files in the folder
files = os.listdir(folder_path)

# Create a list to store the timestamps and ISO speed values
timestamps = []
index =0

# Loop through each file in the folder
for file in files:
    # Get the full path to the file
    file_path = os.path.join(folder_path, file)

    # Check if the file is a JPEG image
    if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
        # Open the file and read the metadata
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)

        # Get the timestamp and ISO speed metadata values
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

        # Store the current timestamp as the previous timestamp
        prev_timestamp = timestamp

        index += 1

# Sort the timestamps in chronologically ascending order
timestamps.sort()

# # Format the timestamps and write both the timestamps and sorted data to a text file for DEBUG purposes
# save_path = f'C:/Users/Echo/Desktop/{today}.txt'
# with open(save_path, 'w') as f:
#     counter = 0
#     for timestamp in timestamps: 
#         dt = datetime.datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S")
#         formatted_timestamp = dt.strftime("%I:%M %p")        
#         f.write(f'{formatted_timestamp}\n')
#         counter += 1
#         if counter % 2 == 0:
#             f.write('\n')

# with open(save_path, 'a') as f:
#     for parent_sap, pole_id, structure_type in sorted_data:
#         f.write(f'{parent_sap} {pole_id}, Type: {structure_type} \n')

############################################# END JPG Extract Code #############################################

# Create csv file from data
# with open('sorted_data.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Pole #', 'SAP', 'Type'])
#     for pole_id, parent_sap, structure_type in sorted_data:
#         writer.writerow([pole_id, parent_sap, structure_type])

# # Create txt file from data
# with open('sorted_data.txt', 'w') as file:
#     for pole_id, parent_sap, structure_type in sorted_data:
#         file.write(f'Pole #: {parent_sap} {pole_id}, Type: {structure_type}\n')


################################## Export to PDF #######################################
pdf_save_path = f'C:/Users/Echo/Desktop/Shot Sheets/Filled Out/{today}'

if not os.path.exists(pdf_save_path):
    os.mkdir(pdf_save_path)

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

for i in range(len(pole_ids)):
    PoleData = str(parent_saps[i]) + ' ' + str(pole_ids[i])
    PoleData_field.append(PoleData)

    if structure_types[i].lower() in ['tower']:
        Tower = 'on'
    else: 
        Tower = 'Off'
    if structure_types[i].lower() in ['frame', 'hframe']:
        Hframe = 'on'
    else: 
        Hframe = 'Off' 
    if structure_types[i].lower() in ['pole']:
        Pole = 'on'
    else: 
        Pole = 'Off'
    if structure_types[i].lower() in ['multi', 'multi-structure', 'multistructure', 'multi structure']:
        Multi = 'on'
    else: 
        Multi = 'Off'

    form_fields = fillpdfs.get_form_fields("PGE 2023.pdf")

    data_dict = {
    'dhFormfield-4055512778': 'Precision Hawk',
    'dhFormfield-4055513106': today_pdf,
    'dhFormfield-4055513200': 'ECHO',
    'dhFormfield-4055516340': PoleData_field[i],
    'dhFormfield-4055516446': '', #Lat
    'dhFormfield-4055516466': '', #Long
    'dhFormfield-4055517287': formatted_sf[i],
    'dhFormfield-4055517747': formatted_ef[i], 
    'dhFormfield-4055517826': '', #Field Notes

    'dhFormfield-4055514808': 'Off', #Steel
    'dhFormfield-4055520694': 'Off', #Concrete
    'dhFormfield-4055520764': 'on', #Wood
    'dhFormfield-4055520768': 'Off', #Fiberglass

    'dhFormfield-4055521364': Tower, #Tower
    'dhFormfield-4055522189': Hframe, #H-Frame
    'dhFormfield-4055522223': Pole, #Pole
    'dhFormfield-4055522230': Multi, #Multi-Structure
    }

    pdf_save_dir = os.path.join(pdf_save_path, parent_saps[i] + '.pdf')

    fillpdfs.write_fillable_pdf('PGE 2023.pdf', pdf_save_dir, data_dict)

print(PoleData_field)

################################ END Export to PDF ##################################


# Keep the browser window open
while True:
    pass


