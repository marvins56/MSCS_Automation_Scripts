# Streamlit Application - Email and Doctors' Shifts Scheduler

This Streamlit application offers functionalities related to email operations and scheduling doctors' shifts. Users can send emails, view their inbox, search emails, automate raise requests, generate doctor shifts, view the generated shifts, and observe statistical analyses of the shifts.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Features](#features)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.10.11 installed
- Gmail API credentials (refer to [Gmail Python Quickstart](https://developers.google.com/gmail/api/quickstart/python) to obtain credentials)

## Installation

1. **Clone the Repository**

   If you haven't already, clone the repository to your local machine.

   \`\`\`
   git clone [https://github.com/marvins56/MSCS_Automation_Scripts.git]
   \`\`\`

2. **Set up a Virtual Environment (optional but recommended)**

   It's a good practice to create a virtual environment for your projects to avoid conflicts between package versions.

   \`\`\`
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   \`\`\`

3. **Install Required Libraries**

   Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary libraries.

   \`\`\`
   `pip install streamlit pandas plotly numpy google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`
   \`\`\`

4. **Gmail API Configuration**

   After obtaining your `credentials.json` from the Gmail API console, place it in the main directory of your application.

## Running the Application

1. **Activate your virtual environment if you have one**

   \`\`\`
   `source venv/bin/activate`  # On Windows, use `venv\Scripts\activate`
   \`\`\`

2. **Run Streamlit App**

   \`\`\`
   `streamlit run app.py`  # Replace app.py with the name of your main script if it's different
   \`\`\`

   The application should open in your default web browser. If not, you can manually open the provided link in the terminal.

## Features

1. **Email Feature**: 
    - Send emails with optional attachments
    - View the inbox
    - Search for specific emails
    - Automate raise request emails

2. **Doctors' Shifts Scheduler**:
    - Generate shifts for specified doctors over a certain date range
    - View generated shifts
    - Display statistics and visualizations related to shifts

---


# Gmail API Utility

This utility provides a set of functions to interact with the Gmail API, allowing users to authenticate, send emails, search for emails, and parse emails' content.

## Features

1. **Authentication with Gmail API**: The app provides a seamless way to authenticate with the Gmail API using OAuth 2.0.
2. **Sending Emails**: Users can send emails with or without attachments.
3. **Searching for Emails**: Users can search for emails based on specific queries.
4. **Reading and Parsing Emails**: The utility can read email content, print its basic information, and save any HTML content or attachments to the local system.

## Requirements

- Google API client library for Python
- Gmail API credentials in `credentials.json`

## How it Works

### Authentication

The application uses OAuth 2.0 to authenticate with the Gmail API. On the first run, the user will be prompted to log in and grant permissions. The app saves the access and refresh tokens in a file named `token.pickle` for future sessions.

### Sending Emails

The utility provides a `send_message` function that allows users to send emails with attachments. The attachments are automatically detected based on their MIME type.

### Searching for Emails

The `search_messages` function can be used to search for emails based on a specific query string. This function returns a list of email message objects that match the query.

### Reading and Parsing Emails

The `read_message` function fetches the content of a specified email, prints its basic information, and saves any HTML content or attachments to a local folder. The folder is named based on the email's subject.

## Utility Functions

1. **get_size_format**: Converts bytes into a human-readable format.
2. **clean**: Cleans a text string by replacing non-alphanumeric characters with underscores. Useful for creating folder names based on email subjects.

## Usage

```python
# Sending an email.
send_message(service, "destination@domain.com", "This is a subject", "This is the body of the email", ["test.txt", "anyfile.png"])

# Searching for emails with a specific query and reading them.
results = search_messages(service, "Python Code")
print(f"Found {len(results)} results.")
for msg in results:
    read_message(service, msg)
