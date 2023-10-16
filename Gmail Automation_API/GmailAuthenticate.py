# Importing necessary libraries for file operations and object serialization
import os
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
    
    return messages

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

    # Print basic email information and create a folder based on the subject.
    if headers:
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                print("From:", value)
            elif name.lower() == "to":
                print("To:", value)
            elif name.lower() == "subject":
                has_subject = True
                folder_name = clean(value)
                folder_counter = 0
                while os.path.isdir(folder_name):
                    folder_counter += 1
                    if folder_name[-2:] == f"_{folder_counter}":
                        folder_name = f"{folder_name[:-len(str(folder_counter))]}_{folder_counter+1}"
                    else:
                        folder_name = f"{folder_name}_{folder_counter}"
                os.mkdir(folder_name)
                print("Subject:", value)
            elif name.lower() == "date":
                print("Date:", value)
    
    # If there's no subject, create a default folder named "email".
    if not has_subject and not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    # Parse email parts (content and attachments).
    parse_parts(service, parts, folder_name, message)
    print("="*50)

# Example usage:
# Sending an email.
send_message(service, "destination@domain.com", "This is a subject", "This is the body of the email", ["test.txt", "anyfile.png"])

# Searching for emails with a specific query and reading them.
# results = search_messages(service, "Python Code")
# print(f"Found {len(results)} results.")
# for msg in results:
#     read_message(service, msg)

# # test send email
send_message(service, "destination@domain.com", "This is a subject", 
            "This is the body of the email", ["test.txt", "anyfile.png"])
# # get emails that match the query you specify
# results = search_messages(service, "Python Code")
# print(f"Found {len(results)} results.")
# # for each email matched, read it (output plain/text to console & save HTML and attachments)
# for msg in results:
#     read_message(service, msg)