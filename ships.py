import pandas as pd
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import emoji
from datetime import datetime

# Read the Excel file
df = pd.read_excel('ships.xlsx')

# Create GUI
root = tk.Tk()
root.title("Sheep Queue Simulation Application")

# Create a label to print the data on the screen
label_text = df.to_string(index=False)
label_text_with_emoji = emoji.emojize("\U0001F6A9 " + label_text.replace('\n', '\n\U0001F6A9 '))
label = scrolledtext.ScrolledText(root, width=80, height=20)
label.insert(tk.END, label_text_with_emoji)
label.pack()

# Create the Ship at Destination button
def ship_at_destination():
    global df
    # Remove the ship at the top of the list
    df.drop(df.index[0], inplace=True)
    
    # Calculate the new ranking
    df['pilot_boarding_time'] = pd.to_datetime(df['pilot_boarding_time'], format='%H:%M:%S').dt.time
    df = df.sort_values(by=['pilot_boarding_time'])
    df['New Ranking'] = range(1, len(df) + 1)
    
    # Update the display
    update_display()

    # Update the Excel file
    df.to_excel('ships.xlsx', index=False)

# Add the Ship at Destination button
ship_at_destination_button = tk.Button(root, text="Ship at Destination", command=ship_at_destination)
ship_at_destination_button.pack()

# Create the Add Ship button
def add_ship():
    global df
    ship_mmsi = simpledialog.askinteger("Add Ship", "Ship MMSI:")
    boarding_time = simpledialog.askstring("Add Ship", "Pilot Boarding Time (HH:MM:SS):")
    lat = simpledialog.askfloat("Add Ship", "Latitude:")
    long = simpledialog.askfloat("Add Ship", "Longitude:")

    # New ship data to be added
    new_ship = {
        'Ship_MMSI': ship_mmsi,
        'pilot_boarding_time': datetime.strptime(boarding_time, '%H:%M:%S').time(),
        'lat': lat,
        'long': long
    }

    # Add the new ship to the DataFrame
    df = pd.concat([df, pd.DataFrame([new_ship])], ignore_index=True)
    df['pilot_boarding_time'] = pd.to_datetime(df['pilot_boarding_time'], format='%H:%M:%S').dt.time
    df = df.sort_values(by=['pilot_boarding_time'])
    df['New Ranking'] = range(1, len(df) + 1)

    # Update the display
    update_display()

    # Update the Excel file
    df.to_excel('ships.xlsx', index=False)

# Add the Add Ship button
add_ship_button = tk.Button(root, text="Add Ship", command=add_ship)
add_ship_button.pack()

# Remove the ship from GUI and Excel file based on the new ranking value
def remove_ship():
    global df
    new_ranking = simpledialog.askinteger("Remove Ship", "Delete  Ranking Value:")
    
    # Find and remove the ship with the specified ranking value from the list
    df = df[df['New Ranking'] != new_ranking]
    
    # Calculate the new ranking
    df['pilot_boarding_time'] = pd.to_datetime(df['pilot_boarding_time'], format='%H:%M:%S').dt.time
    df = df.sort_values(by=['pilot_boarding_time'])
    df['New Ranking'] = range(1, len(df) + 1)
    
    # Update the display
    update_display()

    # Update the Excel file
    df.to_excel('ships.xlsx', index=False)

# Add the Remove Ship button
remove_ship_button = tk.Button(root, text="Remove Ship", command=remove_ship)
remove_ship_button.pack()

def update_display():
    # Update the data
    label.delete(1.0, tk.END)
    updated_label_text = df.to_string(index=False)
    updated_label_text_with_emoji = emoji.emojize("\U0001F6A9 " + updated_label_text.replace('\n', '\n\U0001F6A9 '))
    label.insert(tk.END, updated_label_text_with_emoji)

# Start the GUI
root.mainloop()
