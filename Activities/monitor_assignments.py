import os
import time
from plyer import notification

def monitor_folder(folder_path):
    # List all files in the folder
    all_files = set(os.listdir(folder_path))
    while True:
        # Refresh the file list
        new_all_files = set(os.listdir(folder_path))
        # Check for new files
        new_files = new_all_files - all_files
        if new_files:
            for new_file in new_files:
                send_new_assignment_notification(new_file)
            all_files = new_all_files
        # Wait for 1 minute before checking again
        time.sleep(3)

def send_new_assignment_notification(new_file):
    notification.notify(
        title='New Assignment Added',
        message=f'A new assignment file has been added: {new_file}',
        timeout=10
    )

# Specify the folder path to monitor
folder_path = "C:\\Users\\DELL\\Desktop\\Marvin\\personal"
monitor_folder(folder_path)
