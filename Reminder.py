import tkinter as tk
import json
import os
import tkinter.font as tkFont

REMINDER_FILE = "E:/Github/Reminder system/reminders.json"

def load_reminders():
    if os.path.isfile(REMINDER_FILE):
        with open(REMINDER_FILE, 'r') as file:
            reminders = json.load(file)
            for reminder in reminders:
                reminder_list.insert(tk.END, reminder)

def save_reminder():
    remainders = reminder_list.get(0, tk.END)
    with open(REMINDER_FILE, 'w') as file:
        json.dump(list(remainders), file)

root = tk.Tk()
root.title("Reminder System")
root.geometry("570x470")  # Slightly bigger for better view

# Fonts
label_font = tkFont.Font(family="Helvetica", size=18, weight="bold")
text_font = tkFont.Font(family="Times New Roman", size=12)

# Label
tk.Label(root, text="Enter your Reminder", font=label_font).grid(row=0, column=0, columnspan=2, pady=10)

# Entry
reminder_entry = tk.Entry(root, width=50, font=text_font)
reminder_entry.grid(row=1, column=0, columnspan=2, pady=5)

# Listbox
listbox_frame = tk.Frame(root)
listbox_frame.grid(row=2, column=0, columnspan=2,pady=10)

scrollbar = tk.Scrollbar(listbox_frame,orient=tk.VERTICAL)

reminder_list = tk.Listbox(listbox_frame, width=70, height=15, font=text_font,yscrollcommand=scrollbar.set)
reminder_list.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=reminder_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Load existing reminders
load_reminders()

# Functions
def refresh_Index_number():
    reminder = reminder_list.get(0, tk.END)
    reminder_list.delete(0, tk.END)

    for index, reminder in enumerate(reminder, start=1):
        if ']' in reminder:
            reminder_text = reminder.split(']', 1)[1].strip()
        else:
            reminder_text = reminder
        reminder_list.insert(tk.END, f"{index} ] {reminder_text}")

def add_reminder():
    reminder = reminder_entry.get()
    if reminder:
        print(f"Reminder Successfully Added: {reminder}")
        if "edit_position" in globals():
            reminder_list.insert(edit_position, reminder)
            del globals()["edit_position"]
        else:
            reminder_list.insert(tk.END, reminder)

        reminder_entry.delete(0, tk.END)
        refresh_Index_number()
        save_reminder()

def edit_reminder():
    try:
        # Get the selected index and its text
        selected_reminder_index = reminder_list.curselection()[0]
        selected_text = reminder_list.get(selected_reminder_index)

        # Extract only the reminder text (after the index and ']')
        reminder_text = selected_text.split(']', 1)[1].strip()

        # Insert it back to the Entry box for editing
        reminder_entry.delete(0, tk.END)
        reminder_entry.insert(0, reminder_text)

        # Remove it from the list temporarily
        reminder_list.delete(selected_reminder_index)

        global edit_position
        edit_position = selected_reminder_index

        # Refresh index numbers and save
        refresh_Index_number()
        save_reminder()
    except IndexError:
        print("No reminders selected")

def delete_reminder():
    try:
        selected_reminder_index = reminder_list.curselection()[0]
        reminder_list.delete(selected_reminder_index)
        refresh_Index_number()
        save_reminder()
    except IndexError:
        print("No Reminders Selected")
def clear_reminders():
    reminder_list.delete(0, tk.END)
    save_reminder()
# Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=3, column=0, columnspan=2, pady=10)

# Add the buttons inside the button frame
tk.Button(button_frame, text="Add Reminder", command=add_reminder, font=text_font).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Edit Reminder", command=edit_reminder, font=text_font).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Delete Reminder", command=delete_reminder, font=text_font).grid(row=0, column=2, padx=10)
tk.Button(button_frame, text="Clear All", command=clear_reminders, font=text_font).grid(row=0, column=3, padx=10)

reminder_entry.bind("<Return>",lambda event:add_reminder())
# Start the Tkinter loop
root.mainloop()
