from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import base64
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Google Sheets setup
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("path_to_your_service_account_credentials.json", scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open("Your Google Sheet Name").sheet1

# Function to scrape gas price
def scrape_gas_price():
    url = "https://nsuarb.novascotia.ca/mandates/gasoline-diesel-pricing/gasoline-prices-zone-map#/zone_1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    price_div = soup.find("div", class_="field field--name-field-zone-1-unleaded-min field--type-string field--label-hidden field__item")
    if price_div:
        return price_div.text.strip()
    else:
        return None

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