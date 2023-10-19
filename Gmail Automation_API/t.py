import os
import pickle
import random
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from threading import Thread
from Gmail_Auth.GmailApiIntegration import gmail_authenticate, send_message, search_messages, read_message
import schedule
import time
from threading import Thread
import random
from datetime import datetime, timedelta
# Initialize the Gmail API
service = gmail_authenticate()
email_bodies = {
    "Polite": {
        "body": "I've been reflecting on my accomplishments and growth in the company and believe a salary adjustment would be appropriate. Could we discuss this further?",
        "reasons": "Acknowledgment of accomplishments and growth, initiating a respectful discussion about compensation."
    },
    "Direct": {
        "body": "Given my contributions and industry averages, I'd like to discuss a raise in my salary.",
        "reasons": "Direct reference to contributions and industry averages, aligning the request with market standards."
    },
    "Achievements Highlight": {
        "body": "In the past few months, I've achieved [specific achievements]. I believe these contributions provide significant value to the company and would like to discuss adjusting my salary to reflect this.",
        "reasons": "Emphasis on specific achievements, providing evidence of added value to the company."
    },
    "Market Comparison": {
        "body": "I've recently conducted research on industry salary benchmarks, and it appears that my current compensation may be below the market average for someone with my experience and skills. I'd like to discuss this with you.",
        "reasons": "Use of market research to support the request, highlighting potential salary misalignment with industry standards."
    },
    "Cost of Living Adjustment": {
        "body": "I've noticed that the cost of living has increased over the past year, and my current salary is no longer keeping pace with these changes. I'd like to discuss the possibility of a cost of living adjustment.",
        "reasons": "Addressing the rising cost of living, showing the need for a pay raise to maintain financial well-being in the face of economic changes."
    }
}

def get_email_details(message_id):
    msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers")
    
    details = {}
    for header in headers:
        name = header.get("name").lower()
        value = header.get("value")
        if name in ['from', 'subject']:
            details[name] = value
    return details
def send_email_every_custom_duration(email, body, seconds):
    service = gmail_authenticate()
    while True:

        send_message(service, email, "Request for Salary Raise", body)
        time.sleep(seconds)

shift_types = ["Normal Day", "Long Day", "Night Shift"]
filename = "shifts.txt"

def generate_shifts(doctors, start_date, end_date):
    num_days = (end_date - start_date).days + 1
    shifts = {}
    for day in range(num_days):
        random.shuffle(doctors)
        current_date = start_date + pd.DateOffset(days=day)
        shifts[current_date] = {doc: random.choice(shift_types) for doc in doctors}
    return shifts

def save_shifts_to_file(shifts):
    with open(filename, "w") as file:
        for day, assignments in shifts.items():
            file.write(day.strftime('%Y-%m-%d') + "\n")
            for doctor, shift in assignments.items():
                file.write(f"{doctor}: {shift}\n")
            file.write("-" * 40 + "\n")

def display_shift_statistics(shift_df):
    st.subheader("Shift Distribution")
    shift_count = shift_df.apply(lambda x: x.value_counts())
    fig = px.bar(shift_count, title="Shift Distribution", labels={'index': 'Shift Type', 'value': 'Count'})
    st.plotly_chart(fig)

    # Display individual doctor statistics
    st.subheader("Doctor Shift Assignments")
    st.table(shift_df)




st.title("Doctors' Shifts Scheduler")
# Main Streamlit App
st.title("Combined Streamlit App")

# Main Sidebar Dropdown for feature selection
main_options = ["Home", "Email Feature", "Doctors' Shifts Scheduler"]
main_choice = st.sidebar.selectbox("Choose a Feature", main_options)

if main_choice == "Home":
    st.header("Welcome to the Combined Streamlit App!")
    st.write("""
    This app offers two main functionalities:
    1. **Email Feature**: You can send emails, view your inbox, search emails, and automate the process of asking for a raise.
    2. **Doctors' Shifts Scheduler**: Generate and view doctors' shifts, and see statistical analysis of the shifts.
    Select the desired functionality from the sidebar to get started!
    """)

elif main_choice == "Email Feature":
    # Sidebar for selecting email functionalities
    email_options = ["Send Email", "Inbox", "Search Emails", "Ask for a Raise"]
    email_choice = st.sidebar.selectbox("Choose an option", email_options)

    if email_choice == "Send Email":
        st.subheader("Send Email")

    # Input fields for email details
    destination = st.text_input("Recipient Email")
    subject = st.text_input("Email Subject")
    body = st.text_area("Email Body")
    attachments = st.file_uploader("Upload Attachments", type=["txt", "pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)

    # Send button
    if st.button("Send Email"):
        # Convert uploaded files to a format that your function can handle
        filenames = []
        for attachment in attachments:
            with open(attachment.name, "wb") as f:
                f.write(attachment.getvalue())
            filenames.append(attachment.name)

        # Send the email
        response = send_message(service, destination, subject, body, filenames)
        st.success("Email sent successfully!")

        # Remove temporary files (optional)
        for filename in filenames:
            os.remove(filename)

    elif email_choice == "Inbox":
        st.subheader("Inbox")
        messages = search_messages(service, "in:inbox")
        if messages:
            email_details = [get_email_details(msg['id']) for msg in messages]
            selected_email = st.selectbox("Select an email:", email_details, format_func=lambda x: f"{x['from']} - {x['subject']}")
            selected_index = email_details.index(selected_email)
            read_message(service, messages[selected_index])

    elif email_choice == "Search Emails":
        st.subheader("Search Emails")
        query = st.text_input("Enter your search query:")
        if query:
            messages = search_messages(service, query)
            if messages:
                selected_email_id = st.selectbox("Search results:", [msg['id'] for msg in messages])
                for msg in messages:
                    if msg['id'] == selected_email_id:
                        read_message(service, msg)
                        break

    elif email_choice == "Ask for a Raise":
        st.subheader("Automate Raise Request")

        # Guidance for inputs
        st.info("""
        - Enter your boss's email in the provided field.
        - Choose a predefined email body from the dropdown.
        - Optionally set a custom timeline for the scheduler. If left blank, the default is 3 months.
        """)

        boss_email = st.text_input("Boss's Email")
        selected_template = st.selectbox("Select Email Body Template", list(email_bodies.keys()))
        selected_body = email_bodies[selected_template]["body"]  # Extracting the body text

        # Display reasons (optional, but can be informative for the user)
        st.write("Reasons for this template:")
        st.write(email_bodies[selected_template]["reasons"])

        # Custom scheduler settings
        st.write("Custom Scheduler Settings (default is 3 months):")
        days = st.number_input("Days:", min_value=0, value=0)
        weeks = st.number_input("Weeks:", min_value=0, value=0)
        months = st.number_input("Months:", min_value=0, value=3)
        minutes = st.number_input("Minutes:", min_value=0, value=0)  # New line for minutes input
        total_seconds = (days * 86400) + (weeks * 604800) + (months * 2592000) + (minutes * 60)  # Added minutes to seconds conversion
        if st.button("Set up Scheduler"):
            # Start a separate thread to send emails based on custom duration
            thread = Thread(target=send_email_every_custom_duration, args=(boss_email, email_bodies[selected_template]["body"], total_seconds))
            thread.start()

            # Calculate and display the next scheduled email's date and time
            next_email_date = datetime.now() + timedelta(seconds=total_seconds)
            st.success(f"Scheduler set up successfully! The next email will be sent on {next_email_date.strftime('%Y-%m-%d %H:%M:%S')}")

elif main_choice == "Doctors' Shifts Scheduler":
    # Sidebar for selecting doctor's shifts functionalities
    doctor_options = ["Generate Shifts", "View Current Shifts", "Statistics"]
    doctor_choice = st.sidebar.selectbox("Choose an option", doctor_options)

    if doctor_choice == "Generate Shifts":
        num_doctors = st.number_input("Number of doctors", min_value=1, value=5)
        doctors = [st.text_input(f"Doctor {i+1} Name", f"Doctor {i+1}") for i in range(num_doctors)]
        start_date = st.date_input("Start Date", pd.to_datetime('today') - pd.DateOffset(days=7))
        end_date = st.date_input("End Date", pd.to_datetime('today'))
        if st.button("Generate Shifts"):
            shifts = generate_shifts(doctors, start_date, end_date)
            shift_df = pd.DataFrame(shifts).T
            st.write(shift_df)
            display_shift_statistics(shift_df)
            save_shifts_to_file(shifts)
            st.success("Shifts saved successfully!")
    elif doctor_choice == "View Current Shifts":
        if os.path.exists(filename):
            with open(filename, "r") as file:
                st.text(file.read())
        else:
            st.warning("No shifts data found. Please generate shifts first.")
    elif doctor_choice == "Statistics":
        st.subheader("Shift Statistics")
        if os.path.exists(filename):
            with open(filename, "r") as file:
                st.text(file.read())
            display_shift_statistics(pd.read_csv(filename, delimiter=": "))
