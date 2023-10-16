import imaplib
import email
from email.header import decode_header

def check_email(username, password, search_keyword):
    # Connect to your email server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")  # Use 'imap.gmail.com' for Gmail
    mail.login(username, password)

    # Select the mailbox to search in
    mail.select("inbox")

    # Search for emails containing the search_keyword
    status, email_ids = mail.search(None, f'(BODY "{search_keyword}")')
    email_ids = email_ids[0].split()

    for e_id in email_ids:
        # Fetch the email by ID
        status, email_data = mail.fetch(e_id, '(RFC822)')
        raw_email = email_data[0][1]
        msg = email.message_from_bytes(raw_email)
        subject, encoding = decode_header(msg["subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else 'utf-8')
        print(f"Subject: {subject}")

    # Logout and close the connection
    mail.logout()

# Call the function to check email
check_email("kauta.marvins@gmail.com", "X~88marvin559655~", "assignment")
