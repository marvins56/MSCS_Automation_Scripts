import schedule
import time
from plyer import notification

def send_masters_work_notification():
    notification.notify(
        title='Masters Work Time',
        message='Time to switch to your masters work and reading.',
        timeout=10
    )

# Schedule the notification at 11:05 PM every day
schedule.every().day.at("22:05").do(send_masters_work_notification)

while True:
    schedule.run_pending()
    time.sleep(1)
