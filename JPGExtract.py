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
from pykml import parser
from os import path
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

# # Define the path to the folder containing the photos
# folder_path = f'C:/Users/Echo/Desktop/{today}/DJI_20230330092425_0041_Z.jpg'

############## Use Previous Day ###############
folder_path = f'C:/Users/Echo/Desktop/Test'
###############################################

# Get a list of all the files in the folder
files = os.listdir(folder_path)

# Create a list to store the timestamps and ISO speed values
lat_coordinates = []
lon_coordinates = []

# Specify the namespace used in your KML file
ns = {'ns': 'http://www.opengis.net/kml/2.2'}

lat_list = []
lon_list = []

def dms_to_dd(dms):
    degrees = dms[0]
    minutes = dms[1]
    seconds = dms[2]
    dd = degrees + minutes/60 + seconds/3600
    return dd

def fraction_to_float(fraction):
    """Converts a fraction to a floating-point number."""
    return float(fraction.num / fraction.den)

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

    if name in pole_ids:

        for file in files:
            # Get the full path to the file
            file_path = os.path.join(folder_path, file)

            # Check if the file is a JPEG image
            if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
                # Open the file and read the metadata
                with open(file_path, 'rb') as f:
                    tags = exifread.process_file(f)

                # Get the timestamp and ISO speed metadata values
                latitude = tags.get('GPS GPSLatitude')
                longitude = tags.get('GPS GPSLongitude')

                if latitude and longitude:
                    lat_dms = [fraction_to_float(d) for d in latitude.values]
                    long_dms = [fraction_to_float(d) for d in longitude.values]
                    lat_dd = dms_to_dd(lat_dms)
                    lon_dd = -1*dms_to_dd(long_dms)
                    lat_match = min(lat_list, key=lambda x: abs(x - lat_dd))
                    lon_match = min(lon_list, key=lambda x: abs(x - lon_dd))

                    print("JPG Lat:", lat_dd)
                    print("KML Lat:", lat_match)
                    print('JPG Lon:', lon_dd)
                    print('KML Lon:', lon_match)



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

