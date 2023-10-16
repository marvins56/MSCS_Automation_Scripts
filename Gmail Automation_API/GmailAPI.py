
from .utils import *
from .utils import _approve

def main_menu():
    while True:
        menu_message = (
            "Welcome to the Email Utility. Please choose an option:\n"
            "1. Send an Email.\n"
            "2. Search for Emails.\n"
            "3. Read the content of an Email.\n"
            "4. Exit."
        )

        speak(menu_message)        
        choice = speech_to_text(2).lower()
        if "send" in choice or choice == "1":
            if _approve("Do you really want to send an email?"):
                voice_prompted_email_composition()
            else:
                speak("Email sending cancelled.")
        elif "search" in choice or choice == "2":
            speak("Please provide the search query.")
            query = speech_to_text(2)
            emails = search_messages(service, query)
            speak(f"Found {len(emails)} emails matching the query. The details have been saved to found_emails.txt.")
        elif "read" in choice or choice == "3":
            # Read the content of the selected email
            with open("found_emails.txt", "r") as file:
                email_list = file.readlines()
            speak("Here are the emails found from your last search:")
            speak("".join(email_list))
            speak("Please select an email by number to read its content.")
            selected_email_index = int(speech_to_text(2)) - 1
            if 0 <= selected_email_index < len(emails):
                if _approve("Do you really want to read the content of the selected email?"):
                    read_message(service, emails[selected_email_index])
                else:
                    speak("Email reading cancelled.")
            else:
                speak("Invalid selection.")
        elif "exit" in choice or choice == "4":
            if _approve("Are you sure you want to exit?"):
                speak("Goodbye!")
                break
            else:
                speak("Exiting cancelled. Returning to the main menu.")
        else:
            speak("I'm sorry, I didn't understand that. Please try again.")

# Initialize the Gmail API service
service = gmail_authenticate()

# Call the menu function to start the utility
main_menu()
