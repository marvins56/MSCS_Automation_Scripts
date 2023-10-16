
import os
import schedule
import time
from plyer import notification

def send_notification(task):
    notification.notify(
        title='Scheduled Task',
        message=f'Time for: {task}',
        timeout=10
    )

def read_schedules(filename):
    try:
        with open(filename, 'r') as file:
            return set('task:' + s for s in file.read().split('task:')[1:])
    except FileNotFoundError:
        with open(filename, 'w') as file:
            file.write('Format to enter tasks:\n')
            file.write('task: Your Task\n')
            file.write('time: HH:MM (24-hour format)\n\n')
            file.write('Example:\n')
            file.write('task: Wake up\n')
            file.write('time: 07:00\n')
        print('No schedules found. A new file has been created with instructions.')
        return set()

def set_schedules(schedules):
    schedule.clear()
    for schedule_info in schedules:
        lines = schedule_info.strip().split('\n')
        if len(lines) == 2 and ': ' in lines[0] and ': ' in lines[1]:
            task = lines[0].split(': ')[1]
            time_str = lines[1].split(': ')[1]
            schedule.every().day.at(time_str).do(send_notification, task)
        else:
            print(f"Invalid schedule format:\n{schedule_info}")

filename = 'schedules.txt'
last_mtime = 0
previous_schedules = set()
while True:
    try:
        mtime = os.path.getmtime(filename)
    except FileNotFoundError:
        mtime = 0
    if mtime != last_mtime:
        last_mtime = mtime
        current_schedules = read_schedules(filename)
        new_or_changed_schedules = current_schedules.difference(previous_schedules)
        if new_or_changed_schedules:
            set_schedules(new_or_changed_schedules)
            tasks = [s.strip().split("\n")[0].split(": ")[1] for s in new_or_changed_schedules if len(s.strip().split("\n")) == 2 and ': ' in s.strip().split("\n")[0] and ': ' in s.strip().split("\n")[1]]
            message = 'New or changed alarms have been set for the following tasks:\n' + '\n'.join(tasks)
            notification.notify(
                title='Alarms Updated',
                message=message,
                timeout=10
            )
        previous_schedules = current_schedules

    schedule.run_pending()
    time.sleep(5)
