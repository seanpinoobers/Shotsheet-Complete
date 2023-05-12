import tkinter as tk
from tkcalendar import Calendar
import os.path
import datetime

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
    print('Calendar date:', calendar_date)
    print("Collection date:", folder_date)
    

window = tk.Tk()
window.title("Shotsheet Complete V1.0")
window.geometry("500x700")

date_label = Calendar(window, selectmode="day", year=2023, month=4, day=13)
date_label.pack(pady=(0,10))
date_button = tk.Button(window, text="Select Collection Date", command=lambda: select_date(date_button), name="date_button")
date_button.pack()

# Display the window
window.mainloop()
print(folder_date, date_obj, calendar_date)
