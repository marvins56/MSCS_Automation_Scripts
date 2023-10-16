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
