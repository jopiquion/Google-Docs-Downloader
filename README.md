# Google Docs Downloader

## Overview

This script automates the process of downloading documents from links provided in a spreadsheet, leveraging the Google Docs API for authentication and management. It's designed to streamline the downloading of files for users with a list of document links, automatically updating their statuses upon successful download.

## Features

- **OAuth 2.0 Authentication**: Securely authenticate using Google's OAuth 2.0 mechanism to access Google Docs.
- **Spreadsheet Management**: Read links from a spreadsheet and update their status upon successful download.
- **File Download**: Download files from provided links, automatically renaming them to avoid filesystem conflicts.
- **Automatic Retry for Expired Tokens**: Automatically refreshes the authentication token if expired, ensuring continuous script operation.

## Prerequisites

Before running the script, ensure you have the following:

- Python 3.x installed on your system.
- Required Python libraries: `os`, `pandas`, `requests`, `re`, `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, and `google-api-python-client`.
- A Google Cloud Platform project with the Google Docs API enabled.
- OAuth 2.0 credentials downloaded as a JSON file from the Google Cloud Console.

## Setup

1. **Install Dependencies**:
    ```bash
    pip install pandas requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    ```

2. **OAuth Credentials**:
    - Place your `credentials.json` file (downloaded from Google Cloud Console) in the script directory.
    - On the first run, the script will prompt you to authorize access via a web browser. This will create a `token.json` file for subsequent runs.

3. **Spreadsheet Configuration**:
    - Ensure your spreadsheet contains at least two columns: `Links` (for document links) and `Status` (to mark the download status).
    - Update the script with the path to your spreadsheet and the download directory.

## Usage

Run the script with Python from your terminal:

```bash
python google_docs_downloader.py
```

The script will:
- Authenticate using OAuth 2.0.
- Read each row from the spreadsheet.
- Download documents from links with an empty status.
- Update the spreadsheet with a `done` status upon successful download.

## Customization

- **Download Directory**: Modify `download_dir` in the script to change the default download location.
- **File Naming**: The `clean_filename` function sanitizes filenames from the `Content-Disposition` header. Adjust as needed.

## Troubleshooting

- **Authentication Issues**: Delete `token.json` and re-run the script to re-authenticate if you encounter authentication errors.
- **Spreadsheet Format**: Ensure the spreadsheet follows the expected format and is accessible by the script.

## License

This project is open source and freely available under the MIT License. See the LICENSE file for more details.
