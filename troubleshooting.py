import os

# Get the path to the User directory
user_dir = os.path.expanduser("~")

# Get the path to the desktop directory by joining the User directory path with the "Desktop" folder name
desktop_dir = os.path.join(user_dir, "Desktop")

# Print the path to the desktop directory
print(desktop_dir)

