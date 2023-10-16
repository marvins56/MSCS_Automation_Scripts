from re import search
import re
import time
import requests
from datetime import datetime
import pygame
from langchain.chat_models import ChatOpenAI
import cv2
import speech_recognition as sr  # required to return a string output by taking microphone input from the user
from dotenv import find_dotenv ,load_dotenv
import sounddevice as sd
import numpy as np
import wavio
import os
import keyboard
from datetime import datetime
import pickle
from .utils import speech_to_text
from .utils import speak
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
dotenv_path= find_dotenv()
load_dotenv(dotenv_path)
voice_id = "pNInz6obpgDQGcFmaJgB"
Vid = os.getenv("voice_id")
elevenLabsAPI = os.getenv("elevenLabsAPI")
# Define the scope for Gmail API. This scope allows full access to the Gmail account.
SCOPES = ['https://mail.google.com/']
# A placeholder email address; replace with your own.
our_email = 'genVisual07@gmail.com'

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
def add_attachment(message, filename):
    """
    Add an attachment to the given email message.

    Parameters:
    - message (MIMEMultipart object): The email message to which the attachment should be added.
    - filename (str): The path to the file to be attached.

    Returns:
    - None: The function modifies the 'message' object in-place by adding the attachment.
    """

    # Determine the MIME (Multipurpose Internet Mail Extensions) type of the file.
    # MIME types describe the nature and format of document content.
    content_type, encoding = guess_mime_type(filename)

    # If the MIME type couldn't be determined, or if the file is encoded,
    # default to 'application/octet-stream' (binary stream).
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'

    # Split the MIME type into its main and sub types.
    # For example, "text/plain" would be split into "text" (main type) and "plain" (sub type).
    main_type, sub_type = content_type.split('/', 1)

    # Handle different main MIME types
    if main_type == 'text':
        # If it's a text file, read it as such.
        with open(filename, 'rb') as fp:
            msg = MIMEText(fp.read().decode(), _subtype=sub_type)
    elif main_type == 'image':
        # If it's an image, read it as an image.
        with open(filename, 'rb') as fp:
            msg = MIMEImage(fp.read(), _subtype=sub_type)
    elif main_type == 'audio':
        # If it's an audio, read it as an audio file.
        with open(filename, 'rb') as fp:
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
    else:
        # For all other file types, treat them as a binary stream.
        with open(filename, 'rb') as fp:
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())

    # Extract the base name of the file (e.g., "document.txt" from "/path/to/document.txt").
    filename = os.path.basename(filename)

    # Add necessary headers to indicate that this part of the email is an attachment.
    msg.add_header('Content-Disposition', 'attachment', filename=filename)

    # Attach the file to the email message.
    message.attach(msg)

def voice_select_attachments():
    # Path to the designated folder
    attachments_folder = "attachments_folder"
    
    # Create the folder if it doesn't exist
    if not os.path.exists(attachments_folder):
        os.makedirs(attachments_folder)

    # List all files in the designated folder
    available_files = os.listdir(attachments_folder)
    selected_files = []

    # Read out available files to the user
    speak("Available files for attachment are:")
    for filename in available_files:
        speak(filename)

    while True:
        speak("Please say 'Select [filename]' to choose a file or 'Remove [filename]' to remove a previously selected file. Say 'Done' when you're finished.")
        response = speech_to_text(2)

        # Check for "Done" command
        if response.lower() == "done":
            break

        # Check for "Select" command
        match = re.search(r'select (.+)', response, re.I)
        if match:
            filename = match.group(1)
            if filename in available_files and filename not in selected_files:
                selected_files.append(filename)
                speak(f"{filename} has been selected.")
                continue
            else:
                speak(f"{filename} is not available or already selected.")
                continue

        # Check for "Remove" command
        match = re.search(r'remove (.+)', response, re.I)
        if match:
            filename = match.group(1)
            if filename in selected_files:
                selected_files.remove(filename)
                speak(f"{filename} has been removed from the selection.")
                continue
            else:
                speak(f"{filename} hasn't been selected.")
                continue

    # Return the full paths of the selected files
    return [os.path.join(attachments_folder, filename) for filename in selected_files]


def build_message(destination, obj, body, attachments=[]):
    """
    Build an email message suitable for sending via Gmail API.

    Parameters:
    - destination (str): The recipient's email address.
    - obj (str): The subject of the email.
    - body (str): The body text of the email.
    - attachments (list of str, optional): List of file paths to be attached to the email.

    Returns:
    - dict: A dictionary containing the raw, base64-encoded email message string.
    """
    # Check if there are any attachments to add.
    if not attachments:
        # If no attachments, create a simple text email.
        message = MIMEText(body)
    else:
        # If there are attachments, create a multipart email.
        message = MIMEMultipart()
        # Attach the main body of the email.
        message.attach(MIMEText(body))
        # Add each attachment to the email.
        for filename in attachments:
            add_attachment(message, filename)

    # Set the email headers for recipient, sender, and subject.
    message['to'] = destination
    message['from'] = our_email
    message['subject'] = obj

    # Return the email as a raw, base64-encoded string, suitable for Gmail API.
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

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
def search_messages(service, query):
    """
    Search for email messages in the Gmail inbox based on a given query.

    Parameters:
    - service (googleapiclient.discovery.Resource): The Gmail API service object.
    - query (str): The search query string.

    Returns:
    - list: A list of message objects that match the query.
    """
    
    # Start the search with the provided query.
    result = service.users().messages().list(userId='me', q=query).execute()
    
    messages = []  # List to store found messages.

    # Check if any messages were returned in the initial search.
    if 'messages' in result:
        messages.extend(result['messages'])

    # If there are more pages of results, keep fetching them until we've retrieved them all.
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    
     # Ensure the directory for the file exists or create it.
    if not os.path.exists("found_emails.txt"):
        with open("found_emails.txt", "w") as file:
            pass

    # Save the list of found messages to the text file.
    with open("found_emails.txt", "w") as file:
        for index, message in enumerate(messages, 1):
            email = service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['Subject', 'From']).execute()
            subject = next((header['value'] for header in email['payload']['headers'] if header['name'] == 'Subject'), 'No Subject')
            sender = next((header['value'] for header in email['payload']['headers'] if header['name'] == 'From'), 'Unknown Sender')
            file.write(f"{index}. From: {sender}, Subject: {subject}\n")
    
    return messages
def select_email_from_list():
    # Read out the list of emails from the text file.
    with open("found_emails.txt", "r") as file:
        email_list = file.readlines()
        speak("Here are the found emails:")
        for email in email_list:
            speak(email)

    # Prompt the user to select an email.
    speak("Please say the number of the email you want to select.")
    selected_number = int(speech_to_text(2))

    # Return the selected email.
    if 1 <= selected_number <= len(email_list):
        return email_list[selected_number - 1]
    else:
        speak("Invalid selection.")
        return None
def get_size_format(b, factor=1024, suffix="B"):
    """
    Convert bytes into a human-readable format.

    Parameters:
    - b (int): The size in bytes.
    - factor (int, optional): The conversion factor (default is 1024 for bytes to KB, MB, etc.).
    - suffix (str, optional): The suffix for the smallest unit (default is "B" for bytes).

    Returns:
    - str: The formatted size string.
    """
    
    # Iterate through potential size units.
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"  # Return in Yottabytes if size is extremely large.
def clean(text):
    """
    Clean a text string by replacing non-alphanumeric characters with underscores.

    Parameters:
    - text (str): The input text string.

    Returns:
    - str: The cleaned string.
    """
    
    # Replace non-alphanumeric characters with underscores.
    return "".join(c if c.isalnum() else "_" for c in text)
def parse_parts(service, parts, folder_name, message):
    """
    Recursively parse the content of an email partition and handle different content types 
    like plain text, HTML, and various attachments.

    Parameters:
    - service (googleapiclient.discovery.Resource): The Gmail API service object.
    - parts (list): List of email parts to parse.
    - folder_name (str): Name of the folder where attachments and HTML content will be saved.
    - message (dict): The Gmail API message object.
    """
    
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")

            # If a part has nested parts, process them recursively.
            if part.get("parts"):
                parse_parts(service, part.get("parts"), folder_name, message)
            
            # Handle plain text content.
            if mimeType == "text/plain" and data:
                text = urlsafe_b64decode(data).decode()
                print(text)
            
            # Handle HTML content.
            elif mimeType == "text/html":
                if not filename:
                    filename = "index.html"
                filepath = os.path.join(folder_name, filename)
                print("Saving HTML to", filepath)
                with open(filepath, "wb") as f:
                    f.write(urlsafe_b64decode(data))
            else:
                # Handle attachments.
                for part_header in part_headers:
                    part_header_name = part_header.get("name")
                    part_header_value = part_header.get("value")
                    if part_header_name == "Content-Disposition" and "attachment" in part_header_value:
                        print("Saving the file:", filename, "size:", get_size_format(file_size))
                        attachment_id = body.get("attachmentId")
                        attachment = service.users().messages().attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                        data = attachment.get("data")
                        filepath = os.path.join(folder_name, filename)
                        if data:
                            with open(filepath, "wb") as f:
                                f.write(urlsafe_b64decode(data))
def read_message(service, message):
    """
    Download the content of an email, print basic information, and save HTML and attachments.

    Parameters:
    - service (googleapiclient.discovery.Resource): The Gmail API service object.
    - message (dict): The Gmail API message object.
    """
    
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False
    
    # Extracted content to be read aloud
    from_address = ""
    subject_content = ""
    body_content = ""

    # Extract basic email information and create a folder based on the subject.
    if headers:
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                from_address = f"From: {value}"
            elif name.lower() == "subject":
                has_subject = True
                subject_content = f"Subject: {value}"
                folder_name = clean(value)
                folder_counter = 0
                while os.path.isdir(folder_name):
                    folder_counter += 1
                    if folder_name[-2:] == f"_{folder_counter}":
                        folder_name = f"{folder_name[:-len(str(folder_counter))]}_{folder_counter+1}"
                    else:
                        folder_name = f"{folder_name}_{folder_counter}"
                os.mkdir(folder_name)

    # If there's no subject, create a default folder named "email".
    if not has_subject and not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    # Parse email parts (content and attachments) and extract body content.
    body_content = parse_parts(service, parts, folder_name, message)
    
    # Read aloud the extracted content
    final_content = f"{from_address}\n{subject_content}\n{body_content}"
    speak(final_content)

# def read_message(service, message):
#     """
#     Download the content of an email, print basic information, and save HTML and attachments.

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

#     # Print basic email information and create a folder based on the subject.
#     if headers:
#         for header in headers:
#             name = header.get("name")
#             value = header.get("value")
#             if name.lower() == 'from':
#                 print("From:", value)
#             elif name.lower() == "to":
#                 print("To:", value)
#             elif name.lower() == "subject":
#                 has_subject = True
#                 folder_name = clean(value)
#                 folder_counter = 0
#                 while os.path.isdir(folder_name):
#                     folder_counter += 1
#                     if folder_name[-2:] == f"_{folder_counter}":
#                         folder_name = f"{folder_name[:-len(str(folder_counter))]}_{folder_counter+1}"
#                     else:
#                         folder_name = f"{folder_name}_{folder_counter}"
#                 os.mkdir(folder_name)
#                 print("Subject:", value)
#             elif name.lower() == "date":
#                 print("Date:", value)
    
#     # If there's no subject, create a default folder named "email".
#     if not has_subject and not os.path.isdir(folder_name):
#         os.mkdir(folder_name)

#      # Parse email parts (content and attachments).
#     content_to_read += parse_parts(service, parts, folder_name, message)
#     print("="*50)

#     # Read the gathered content aloud.
#     speak(content_to_read)

def voice_prompted_email_composition():
    # Authenticate with Gmail API
    # service = gmail_authenticate()
    # Voice prompt for recipient's email
    speak("Please say the recipient's email address.")
    recipient = speech_to_text(2)

    # Confirm the recipient email
    if not _approve(f"You said the recipient's email is: {recipient}. Do you approve?"):
        speak("Please repeat the recipient's email address.")
        recipient = speech_to_text(2)

    # Voice prompt for email subject
    speak("Please say the subject of the email.")
    subject = speech_to_text(2)

    # Confirm the subject
    if not _approve(f"You said the subject is: {subject}. Do you approve?"):
        speak("Please repeat the subject of the email.")
        subject = speech_to_text(2)

    # Voice prompt for email body
    speak("Please say the body of the email.")
    body = speech_to_text(2)

    # Confirm the body
    if not _approve(f"You said the body is: {body}. Do you approve?"):
        speak("Please repeat the body of the email.")
        body = speech_to_text(4)

    # Voice prompt for attachments
    speak("Do you want to attach any files? Say 'Yes' or 'No'.")
    attachment_response = speech_to_text(2)
    attachments = []
    if attachment_response.lower() in ("yes", "y"):
        attachments = voice_select_attachments()

    # Confirm sending the email
    confirmation_message = (
        f"You are about to send an email to {recipient} with the subject {subject} "
        f"and the following attachments: {', '.join(attachments) if attachments else 'None'}. "
        f"Do you approve?"
    )
    if _approve(confirmation_message):
        try:
            send_message(service, recipient, subject, body, attachments)
            speak("Email sent successfully!")
        except Exception as e:
            speak(f"An error occurred while sending the email: {str(e)}")
    else:
        speak("Email sending cancelled.")
def _approve(_input: str) -> bool:
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.energy_threshold = 200
            r.pause_threshold = 0.5
            msg = (
                "Do you approve of the following input? "
                "Please say 'Yes' or 'No'  within 30 seconds."
            )
            msg += "\n\n" + _input + "\n"
            speak(msg)
            try:
                audio = r.listen(source, timeout=30, phrase_time_limit=30)
                resp = r.recognize_google(audio)
                return resp.lower() in ("yes", "y")
            except Exception as e:
                print(f"An error occurred while recognizing your response: {e}")
                return False
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
def speak(text):
    # if current_language.lower == "english":
        voice_id = Vid
        api_key = elevenLabsAPI
        CHUNK_SIZE = 1024
        
        # filename = now.strftime("%Y-%m-%d_%H-%M-%S")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_file = f'{timestamp}.mp3'
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            speak(f"HTTP error occurred: {err}")
            return
        except Exception as err:
            speak(f"An error occurred: {err}")
            return

        try:

            directory = datetime.now().strftime('%Y-%m-%d')
            os.makedirs(directory, exist_ok=True)

            file_path = os.path.join(directory, output_file)

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

            # Play the audio file with pygame
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue

            pygame.mixer.quit()  # Release the audio file after playing

            # Delete the audio file after it's been played
            try:
                os.remove(file_path)
            except Exception as err:
                print(f"An error occurred while deleting the file: {err}")

        except Exception as err:
            print(f"An error occurred: {err}")
def speech_to_text(pause_threshold):
    # Initialize speech recognizer
    r = sr.Recognizer()
    # Use default system microphone as source to listen to speech
    with sr.Microphone() as source:
        speak("Listening.... Now..")
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source)
        # Record the user's speech
        r.adjust_for_ambient_noise(source)
        r.energy_threshold = 200
        r.pause_threshold = pause_threshold
        audio = r.listen(source)
    try:
        # Use Google speech recognition to convert speech to text
        text = r.recognize_google(audio)
        # speak(f"You said: {text}")
        # speak("Noted.")
        return text

    except sr.UnknownValueError:
        speak("Sorry, could not understand your input.")
    except sr.RequestError:
        speak("Sorry, there was an error with the speech recognition service.")

        # Return empty string on error
        return ""
    