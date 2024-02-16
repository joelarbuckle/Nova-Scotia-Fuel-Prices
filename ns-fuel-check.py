from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import base64
import os

# Function to create a Gmail service
def create_gmail_service():
    creds = Credentials.from_service_account_file('path_to_your_service_account_credentials.json', scopes=['https://www.googleapis.com/auth/gmail.send'])
    service = build('gmail', 'v1', credentials=creds)
    return service

# Function to send email using Gmail API
def send_email_gmail_api(recipients, change):
    service = create_gmail_service()
    sender = "your_email@example.com"
    subject = "Gas Price Change Notification"
    body = f"Dear user,\n\nThe gas price has changed by {change}.\n\nBest regards."

    for recipient in recipients:
        mime_message = MIMEText(body)
        mime_message['to'] = recipient
        mime_message['subject'] = subject
        raw_string = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

        try:
            message = service.users().messages().send(userId="me", body={'raw': raw_string}).execute()
            print(f"Message Id: {message['id']}")
        except HttpError as error:
            print(f'An error occurred: {error}')

# Replace the call to send_email in the main function with send_email_gmail_api
def main():
    price = scrape_gas_price()
    if price:
        change = update_sheet(price)
        if change != 0:
            recipients = ["recipient1@example.com", "recipient2@example.com"]
            send_email_gmail_api(recipients, change)

if __name__ == "__main__":
    main()