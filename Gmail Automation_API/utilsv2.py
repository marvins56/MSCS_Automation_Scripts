
import streamlit as st
from newUtils import *

import streamlit as st
def list_emails(service):
    """
    List the recent emails in the Gmail inbox.

    Parameters:
    - service (googleapiclient.discovery.Resource): The Gmail API service object.

    Returns:
    - list: A list of email summaries.
    """

    # Get a list of the recent emails.
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    email_summaries = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        email_data = msg['payload']['headers']

        for values in email_data:
            name = values['name']
            if name == 'From':
                from_ = values['value']
            if name == 'Subject':
                subject = values['value']

        email_summaries.append((msg['id'], f"From: {from_}, Subject: {subject}"))

    return email_summaries

def main():
    st.title("Gmail API Streamlit App")
    
    # Create a sidebar for navigation
    menu = ["Home", "Send Email", "Search Emails", "Read Emails"]
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


if __name__ == "__main__":
    main()
