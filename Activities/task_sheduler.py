

import os
import time
import shutil
from datetime import datetime, timedelta
from plyer import notification
import schedule
import tkinter as tk
from tkinter import simpledialog, messagebox
from dateutil import parser

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_due_date():
    root = tk.Tk()
    root.withdraw()
   
    # Create a simple dialog for date input
    due_date_str = simpledialog.askstring("Due Date", "Enter due date in YYYY-MM-DD HH:MM format:", parent=root)
    
    if due_date_str:
        try:
            due_date = parser.parse(due_date_str)
            return due_date.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            # Handle invalid date format
            messagebox.showerror("Invalid Date", "Please enter a valid date in the format YYYY-MM-DD HH:MM.")
    return None

def send_assignment_detected_notification(filename):
    notification.notify(
        title='New Assignment Detected',
        message=f'A new assignment file has been detected: {filename}',
        timeout=10
    )

def monitor_folder(folder_path, partial_path, complete_path):
    create_folder(folder_path)
    create_folder(partial_path)
    create_folder(complete_path)
    
    all_files = set(os.listdir(folder_path))
    while True:
        new_all_files = set(os.listdir(folder_path))
        new_files = new_all_files - all_files
        if new_files:
            for new_file in new_files:
                send_assignment_detected_notification(new_file)
                due_date = get_due_date()
                if due_date:
                    due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
                    schedule_assignment(folder_path, partial_path, new_file, due_date)
            all_files = new_all_files
        time.sleep(2)

def schedule_assignment(folder_path, partial_path, filename, due_date):
    reminder_time = due_date - timedelta(minutes=10)
    schedule.every().day.at(reminder_time.strftime("%H:%M")).do(
        send_reminder, filename, due_date.strftime("%Y-%m-%d %H:%M")
    )
    schedule.every().day.at(due_date.strftime("%H:%M")).do(
        move_file, os.path.join(folder_path, filename), partial_path
    )

def send_reminder(filename, due_date):
    notification.notify(
        title='Assignment Reminder',
        message=f'The due date for assignment {filename} is on {due_date}.',
        timeout=10
    )

def move_file(file_path, dest_folder):
    shutil.move(file_path, os.path.join(dest_folder, os.path.basename(file_path)))
    notification.notify(
        title='Assignment Moved',
        message=f'The assignment {os.path.basename(file_path)} has been moved to {dest_folder}.',
        timeout=10
    )

folder_path = 'C:\\Users\\DELL\\Desktop\\Marvin\\TestMasters'
partial_path = 'C:\\Users\\DELL\\Desktop\\Marvin\\TestMasters\\partialComplete'
complete_path = 'C:\\Users\\DELL\\Desktop\\Marvin\\TestMasters\\completeTasks'



monitor_folder(folder_path, partial_path, complete_path)
