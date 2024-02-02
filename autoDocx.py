import os
import pandas as pd
import requests
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def clean_filename(content_disposition, default_name):
    """Extract and clean the filename from the Content-Disposition header."""
    if 'filename=' in content_disposition:
        filename = re.findall('filename="(.+)"', content_disposition)
        if filename:
            return filename[0].replace('/', '_').replace('\\', '_')
    return default_name

# Define the download directory
download_dir = 'path_to_download_folder_for_docs'

# OAuth 2.0 Setup
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
CLIENT_SECRET_FILE = 'path_to_file'
creds = None

# Check for existing token, refresh or create new token as necessary
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Accessing Google Docs API for authentication
service = build('docs', 'v1', credentials=creds)

# Load the spreadsheet
df = pd.read_excel('path_to_spreadsheet')

# Iterate through each row
for index, row in df.iterrows():
    # Process only if the status is blank
    if pd.isna(row['Status']) or row['Status'].strip() == '':
        link = row['Links']
        print(f"Processing link: {link}")

        try:
            # Visit the link and initiate download
            response = requests.get(link, stream=True)
            print(f"Response status code: {response.status_code}")

            # Check if the request was successful
            if response.status_code == 200:
                content_disposition = response.headers.get('content-disposition', '')
                filename = clean_filename(content_disposition, f'download_{index}.ext')
                print(f"Downloading file: {filename}")

                # Save the file
                with open(os.path.join(download_dir, filename), 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                # Update the status to 'done'
                df.at[index, 'Status'] = 'done'
        except Exception as e:
            print(f"Failed to download from {link}: {e}")

# Save the updated spreadsheet
df.to_excel('path_to_spreadsheet', index=False)
