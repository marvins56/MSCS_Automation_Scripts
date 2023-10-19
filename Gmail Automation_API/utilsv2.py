


import streamlit as st
from newUtils import *
import datetime
import schedule
import time
import threading

def send_schedule_notification(service):
    # Define recipient, subject, and body for the notification email
    recipient = 'your_email_address_here'
    subject = 'Email Scheduling Notification'
    body = 'Your email has been scheduled successfully!'
    
    # Send the notification email
    send_message(service, recipient, subject, body)

def schedule_email(service, start_date, frequency):
    # Calculate the time difference between now and the start_date
    delay = (start_date - datetime.datetime.now()).total_seconds()

    # Schedule the email based on the delay and frequency
    schedule.every(frequency).weeks.do(request_raise_email, service).tag("email_job")

    # Send an initial notification about the scheduling
    send_schedule_notification(service)

    # Sleep until the start_date, then run the pending tasks
    time.sleep(delay)
    while True:
        schedule.run_pending()
        time.sleep(1)  # Check every second for scheduled tasks

def main():
    st.title("Gmail API Streamlit App")
    
    # Create a sidebar for navigation
    menu = ["Home", "Send Email", "Search Emails", "Read Emails", "Schedule Emails"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.write("Welcome to the Gmail API Streamlit App!")

    elif choice == "Send Email":
        st.subheader("Compose and Send Email")
        email_composition()

    elif choice == "Search Emails":
        st.subheader("Search Emails in Inbox")
        messages = search_messages(service)
        if messages:
            st.write("Select a message to view its content:")
            for message in messages:
                if st.button(f"View message {message['id']}"):
                    read_message_ui(service, message)

    elif choice == "Read Emails":
        st.subheader("Read Emails from Inbox")
        email_summaries = list_emails(service)
        for email_id, summary in email_summaries:
            if st.button(summary, key=email_id):
                message = {'id': email_id}
                read_message_ui(service, message)

    elif choice == "Schedule Emails":
        st.subheader("Schedule Email Automation")
        
        start_date = st.date_input("Select a start date for the email:")
        frequency = st.slider("Select frequency (in weeks) for the email:", 1, 52, 12)  # default to every 3 months

        if st.button("Schedule Email"):
            # Run the scheduler in a separate thread to avoid blocking the Streamlit app
            t = threading.Thread(target=schedule_email, args=(service, start_date, frequency))
            t.start()
            st.success(f"Email scheduled to start on {start_date} and repeat every {frequency} weeks!")

if __name__ == "__main__":
    main()
