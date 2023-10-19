
from re import search
import re
import time
import requests
from datetime import datetime

import speech_recognition as sr  # required to return a string output by taking microphone input from the user
# from dotenv import find_dotenv ,load_dotenv
import datetime
import schedule
import time
import threading
import numpy as np
import wavio
import os
import keyboard
from datetime import datetime
import pickle

# Importing Gmail API utilities
# `build` helps in constructing the service object for accessing various services.
from googleapiclient.discovery import build
# `InstalledAppFlow` is used to manage the OAuth2.0 flow.
from google_auth_oauthlib.flow import InstalledAppFlow
# `Request` helps in making authenticated requests using the credentials.
from google.auth.transport.requests import Request
# Libraries for encoding/decoding messages in base64 format.
# This is important because email content and attachments are often encoded in base64.
from base64 import urlsafe_b64decode, urlsafe_b64encode
# Libraries for dealing with email content and attachments based on their MIME (Multipurpose Internet Mail Extensions) types.
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
# To identify the MIME type based on file extension.
from mimetypes import guess_type as guess_mime_type


# dotenv_path= find_dotenv()
# load_dotenv(dotenv_path)
# Vid = os.getenv("voice_id")
# elevenLabsAPI = os.getenv("elevenLabsAPI")
# Define the scope for Gmail API. This scope allows full access to the Gmail account.
SCOPES = ['https://mail.google.com/']
# A placeholder email address; replace with your own.
our_email = 'genVisual07@gmail.com'

# def gmail_authenticate():
#     # Initialize credentials to None.
#     creds = None
#     # Check if the token.pickle file exists.
#     # This file contains the user's access and refresh tokens.
#     # It's created automatically after the first successful authorization.
#     if os.path.exists("token.pickle"):
#         with open("token.pickle", "rb") as token:
#             creds = pickle.load(token)  # Load credentials from the file.

#     # If no valid credentials are available, prompt the user for login.
#     if not creds or not creds.valid:
#         # If credentials are expired but a refresh token is available, refresh the credentials.
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             # Begin the OAuth2.0 flow.
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'C:\\Users\\DELL\\Desktop\\Marvin\\MSCS\\masters assignment\\Activities\\credentials.json', 
#                 SCOPES)
#             creds = flow.run_local_server(port=0)  # Authenticate and get the credentials.
        
#         # Save the obtained credentials for future use.
#         with open("token.pickle", "wb") as token:
#             pickle.dump(creds, token)

#     # Return a service object using the credentials which can be used to interact with the Gmail API.
#     return build('gmail', 'v1', credentials=creds)

# # Authenticate and get the Gmail API service object to perform Gmail operations.
# service = gmail_authenticate()
# # Adds the attachment with the given filename to the given message

# import streamlit as st
# def email_composition():
#     # Authenticate with Gmail API
#     # service = gmail_authenticate()

#     # UI for recipient's email
#     recipient = st.text_input("Recipient's email address:")

#     # UI for email subject
#     subject = st.text_input("Subject of the email:")

#     # UI for email body
#     body = st.text_area("Body of the email:")

#     # UI for attachments
#     attachments = []
#     if st.checkbox("Do you want to attach any files?"):
#         uploaded_files = st.file_uploader("Choose files to attach:", accept_multiple_files=True)
#         for uploaded_file in uploaded_files:
#             # The uploaded_file is a BytesIO object. You might want to save it or convert it as per your needs.
#             attachments.append(uploaded_file.name)

#     # UI for sending the email
#     if st.button("Send Email"):
#         confirmation_message = (
#             f"You are about to send an email to {recipient} with the subject {subject} "
#             f"and the following attachments: {', '.join(attachments) if attachments else 'None'}. "
#             f"Do you approve?"
#         )
#         if st.checkbox("Confirm sending the email") and st.button("Confirm"):
#             try:
#                 # Modify send_message to accommodate the changes if needed.
#                 send_message(service, recipient, subject, body, attachments)
#                 st.success("Email sent successfully!")
#             except Exception as e:
#                 st.error(f"An error occurred while sending the email: {str(e)}")

# def read_message_ui(service, message):
#     """
#     Download the content of an email, display basic information, and offer downloads for attachments.

#     Parameters:
#     - service (googleapiclient.discovery.Resource): The Gmail API service object.
#     - message (dict): The Gmail API message object.
#     """
    
#     msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
#     payload = msg['payload']
#     headers = payload.get("headers")
#     parts = payload.get("parts")
#     folder_name = "email"
#     has_subject = False
    
#     # Extracted content to be displayed
#     from_address = ""
#     subject_content = ""
#     body_content = ""

#     # Extract basic email information and create a folder based on the subject.
#     if headers:
#         for header in headers:
#             name = header.get("name")
#             value = header.get("value")
#             if name.lower() == 'from':
#                 from_address = f"From: {value}"
#             elif name.lower() == "subject":
#                 has_subject = True
#                 subject_content = f"Subject: {value}"
#                 folder_name = clean(value)
#                 folder_counter = 0
#                 while os.path.isdir(folder_name):
#                     folder_counter += 1
#                     if folder_name[-2:] == f"_{folder_counter}":
#                         folder_name = f"{folder_name[:-len(str(folder_counter))]}_{folder_counter+1}"
#                     else:
#                         folder_name = f"{folder_name}_{folder_counter}"
#                 os.mkdir(folder_name)

#     # If there's no subject, create a default folder named "email".
#     if not has_subject and not os.path.isdir(folder_name):
#         os.mkdir(folder_name)

#     # Parse email parts (content and attachments) and extract body content.
#     body_content = parse_parts(service, parts, folder_name, message)
    
#     # Display the extracted content using Streamlit
#     st.write(from_address)
#     st.write(subject_content)
#     st.write(body_content)
    
#     # If there are attachments, provide a download link through Streamlit (This part is a placeholder and needs adjustment based on your `parse_parts` function).
#     if parts:  # assuming parts contain attachments
#         with st.expander("Attachments"):
#             for part in parts:
#                 # Adjust this to correctly get the attachment filename and provide a download link
#                 st.download_button(label="Download", data=part, file_name="attachment_name_here", mime="application/octet-stream")





# def send_message(service, destination, obj, body, attachments=[]):
#     """
#     Send an email via Gmail API.

#     Parameters:
#     - service (googleapiclient.discovery.Resource): The Gmail API service object.
#     - destination (str): The recipient's email address.
#     - obj (str): The subject of the email.
#     - body (str): The body text of the email.
#     - attachments (list of str, optional): List of file paths to be attached to the email.

#     Returns:
#     - dict: Gmail API response after sending the email.
#     """

#     # Use the Gmail API service to send the constructed email message.
#     return service.users().messages().send(
#       userId="me",
#       body=build_message(destination, obj, body, attachments)
#     ).execute()
# def search_messages(service):
#     """
#     Search for email messages in the Gmail inbox based on a user-provided query.

#     Parameters:
#     - service (googleapiclient.discovery.Resource): The Gmail API service object.

#     Returns:
#     - list: A list of message objects that match the query.
#     """
    
#     # Provide a search bar for the user to input their query.
#     query = st.text_input("Enter your search query:")

#     if st.button("Search"):
#         # Start the search with the provided query.
#         result = service.users().messages().list(userId='me', q=query).execute()
        
#         messages = []  # List to store found messages.

#         # Check if any messages were returned in the initial search.
#         if 'messages' in result:
#             messages.extend(result['messages'])

#         # If there are more pages of results, keep fetching them until we've retrieved them all.
#         while 'nextPageToken' in result:
#             page_token = result['nextPageToken']
#             result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
#             if 'messages' in result:
#                 messages.extend(result['messages'])

#         # Display the list of found messages in Streamlit.


#         if not os.path.exists("found_emails.txt"):
#             with open("found_emails.txt", "w") as file:
#                 pass
            
#         for index, message in enumerate(messages, 1):
#             email = service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['Subject', 'From']).execute()
#             subject = next((header['value'] for header in email['payload']['headers'] if header['name'] == 'Subject'), 'No Subject')
#             sender = next((header['value'] for header in email['payload']['headers'] if header['name'] == 'From'), 'Unknown Sender')
#             st.write(f"{index}. From: {sender}, Subject: {subject}")
        
#         return messages

#     else:
#         return []


# def select_email_from_list():
#     """
#     Display a list of emails from the text file and allow the user to select one.

#     Returns:
#     - str: The selected email.
#     """
#     # Read the list of emails from the text file.
#     with open("found_emails.txt", "r") as file:
#         email_list = [email.strip() for email in file.readlines()]

#     # Use Streamlit to display the list and get the user's selection.
#     selected_email = st.selectbox("Select an email from the list:", email_list)

#     if st.button("Confirm Selection"):
#         return selected_email




# def get_size_format(b, factor=1024, suffix="B"):
#     """
#     Convert bytes into a human-readable format.

#     Parameters:
#     - b (int): The size in bytes.
#     - factor (int, optional): The conversion factor (default is 1024 for bytes to KB, MB, etc.).
#     - suffix (str, optional): The suffix for the smallest unit (default is "B" for bytes).

#     Returns:
#     - str: The formatted size string.
#     """
    
#     # Iterate through potential size units.
#     for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
#         if b < factor:
#             return f"{b:.2f}{unit}{suffix}"
#         b /= factor
#     return f"{b:.2f}Y{suffix}"  # Return in Yottabytes if size is extremely large.
# def clean(text):
#     """
#     Clean a text string by replacing non-alphanumeric characters with underscores.

#     Parameters:
#     - text (str): The input text string.

#     Returns:
#     - str: The cleaned string.
#     """
    
#     # Replace non-alphanumeric characters with underscores.
#     return "".join(c if c.isalnum() else "_" for c in text)

# def parse_parts(service, parts, folder_name, message):
#     """
#     Recursively parse the content of an email partition and handle different content types 
#     like plain text, HTML, and various attachments.

#     Parameters:
#     - service (googleapiclient.discovery.Resource): The Gmail API service object.
#     - parts (list): List of email parts to parse.
#     - folder_name (str): Name of the folder where attachments and HTML content will be saved.
#     - message (dict): The Gmail API message object.
#     """
    
#     if parts:
#         for part in parts:
#             filename = part.get("filename")
#             mimeType = part.get("mimeType")
#             body = part.get("body")
#             data = body.get("data")
#             file_size = body.get("size")
#             part_headers = part.get("headers")

#             # If a part has nested parts, process them recursively.
#             if part.get("parts"):
#                 parse_parts(service, part.get("parts"), folder_name, message)
            
#             # Handle plain text content.
#             if mimeType == "text/plain" and data:
#                 text = urlsafe_b64decode(data).decode()
#                 st.write(text)
            
#             # Handle HTML content.
#             elif mimeType == "text/html":
#                 if not filename:
#                     filename = "index.html"
#                 filepath = os.path.join(folder_name, filename)
#                 with open(filepath, "wb") as f:
#                     f.write(urlsafe_b64decode(data))
#                 st.write(f"HTML content saved as: {filename}")
#                 st.download_button("Download HTML", data=urlsafe_b64decode(data), file_name=filename, mime="text/html")
            
#             # 
#             else:
#             # Handle attachments.
#                 for part_header in part_headers:
#                     part_header_name = part_header.get("name")
#                     part_header_value = part_header.get("value")
#                     if part_header_name == "Content-Disposition" and "attachment" in part_header_value:
#                         attachment_id = body.get("attachmentId")
#                         attachment = service.users().messages().attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
#                         data = attachment.get("data")
#                         if data:
#                             binary_data = urlsafe_b64decode(data)
#                             filepath = os.path.join(folder_name, filename)
#                             with open(filepath, "wb") as f:
#                                 f.write(binary_data)
#                             st.write(f"Attachment saved as: {filename}")
#                             st.download_button("Download Attachment", data=binary_data, file_name=filename, mime=mimeType)
#             # else:
#             # # Handle attachments.
#             #     for part_header in part_headers:
#             #         part_header_name = part_header.get("name")
#             #         part_header_value = part_header.get("value")
#             #         if part_header_name == "Content-Disposition" and "attachment" in part_header_value:
#             #             attachment_id = body.get("attachmentId")
#             #             attachment = service.users().messages().attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
#             #             data = attachment.get("data")
#             #             if data:
#             #                 binary_data = urlsafe_b64decode(data)
#             #                 filepath = os.path.join(folder_name, filename)
#             #                 with open(filepath, "wb") as f:
#             #                     f.write(binary_data)
#             #                 st.write(f"Attachment saved as: {filename}")
# def request_raise_email(service):
#     # Define your boss's email
#     boss_email = 'boss@example.com'
    
#     # Define the subject and body of the email
#     subject = 'Request for Salary Raise'
#     body = """
#     Dear [Boss's Name],

#     I hope this email finds you well. As we approach the end of another quarter, 
#     I wanted to discuss the possibility of a salary raise based on my contributions and 
#     the increased responsibilities I've undertaken.

#     [Your justification for the raise.]

#     Thank you for considering my request. I look forward to discussing this further with you.

#     Best Regards,
#     [Your Name]
#     """
    
#     # Attachments (if any)
#     attachments = []  # Currently no attachments; add paths to files if needed

#     # Use the existing method to send the email
#     send_message(service, boss_email, subject, body, attachments)

# def schedule_email(service, start_date, frequency):
#     # Calculate the time difference between now and the start_date
#     delay = (start_date - datetime.datetime.now()).total_seconds()

#     # Schedule the email based on the delay and frequency
#     schedule.every(frequency).weeks.do(request_raise_email, service).tag("email_job")

#     # Sleep until the start_date, then run the pending tasks
#     time.sleep(delay)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)  # Check every second for scheduled tasks

# def list_emails(service):
#     """
#     List the recent emails in the Gmail inbox.

#     Parameters:
#     - service (googleapiclient.discovery.Resource): The Gmail API service object.

#     Returns:
#     - list: A list of email summaries.
#     """

#     # Get a list of the recent emails.
#     results = service.users().messages().list(userId='me', maxResults=10).execute()
#     messages = results.get('messages', [])

#     email_summaries = []
#     for message in messages:
#         msg = service.users().messages().get(userId='me', id=message['id']).execute()
#         email_data = msg['payload']['headers']

#         for values in email_data:
#             name = values['name']
#             if name == 'From':
#                 from_ = values['value']
#             if name == 'Subject':
#                 subject = values['value']

#         email_summaries.append((msg['id'], f"From: {from_}, Subject: {subject}"))




def gmail_authenticate():
    # Initialize credentials to None.
    creds = None
    # Check if the token.pickle file exists.
    # This file contains the user's access and refresh tokens.
    # It's created automatically after the first successful authorization.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)  # Load credentials from the file.

    # If no valid credentials are available, prompt the user for login.
    if not creds or not creds.valid:
        # If credentials are expired but a refresh token is available, refresh the credentials.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Begin the OAuth2.0 flow.
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:\\Users\\DELL\\Desktop\\Marvin\\MSCS\\masters assignment\\Activities\\credentials.json', 
                SCOPES)
            creds = flow.run_local_server(port=0)  # Authenticate and get the credentials.
        
        # Save the obtained credentials for future use.
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    # Return a service object using the credentials which can be used to interact with the Gmail API.
    return build('gmail', 'v1', credentials=creds)

# Authenticate and get the Gmail API service object to perform Gmail operations.
service = gmail_authenticate()
# Adds the attachment with the given filename to the given message

def send_message(service, destination, obj, body, attachments=[]):
    """
    Send an email via Gmail API.

    Parameters:
    - service (googleapiclient.discovery.Resource): The Gmail API service object.
    - destination (str): The recipient's email address.
    - obj (str): The subject of the email.
    - body (str): The body text of the email.
    - attachments (list of str, optional): List of file paths to be attached to the email.

    Returns:
    - dict: Gmail API response after sending the email.
    """

    # Use the Gmail API service to send the constructed email message.
    return service.users().messages().send(
      userId="me",
      body=build_message(destination, obj, body, attachments)
    ).execute()

send_message(service,"ökmarvins@gmail.com","test","test")
        