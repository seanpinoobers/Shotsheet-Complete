from datetime import datetime as dT
import datetime
import tkinter as tk
import configparser

today_date = f'{dT.today():%B %d, %Y}'.replace(' 0',' ')
print(today_date)


main_window = tk.Tk()
main_window.title("ShotSheet AutoComplete V 1.0")
main_window.geometry('1388x768')

def yes_button():
    exit()

Text = tk.Label(main_window, text='Hello World!')
Button = tk.Button(main_window, text='Click Here', command=yes_button)

Text.pack()
Button.pack()

main_window.mainloop()



# def save_settings():
#     # code to save settings and update variables
#     option1_value = option1.get()
#     option2_value = option2_var.get()

#     # create configparser object
#     config = configparser.ConfigParser()

#     # add section and options to configparser object
#     config.add_section('Settings')
#     config.set('Settings', 'Option1', option1_value)
#     config.set('Settings', 'Option2', option2_value)

#     # write configparser object to file
#     with open('settings.ini', 'w') as configfile:
#         config.write(configfile)

# def create_settings_window():
#     # create window
#     settings_window = tk.Toplevel()

#     # create widgets
#     label1 = tk.Label(settings_window, text="Option 1")
#     option1 = tk.Entry(settings_window)
#     label2 = tk.Label(settings_window, text="Option 2")
#     option2 = tk.Checkbutton(settings_window, text="Option 2")

#     # add widgets to window
#     label1.pack()
#     option1.pack()
#     label2.pack()
#     option2.pack()

#     # create button to save settings
#     save_button = tk.Button(settings_window, text="Save", command=save_settings)
#     save_button.pack()

#     # run window
#     settings_window.mainloop()

# # create main window
# root = tk.Tk()

# # create button to open settings window
# settings_button = tk.Button(root, text="Settings", command=create_settings_window)
# settings_button.pack()

# # run main window
# root.mainloop()