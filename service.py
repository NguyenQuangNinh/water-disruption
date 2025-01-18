import bs4
import os
import requests
from hashlib import md5
import boto3
import schedule_repository


def format_content(contents):
    # Indent level for each line
    indent = "  "

    # Replace special characters with desired formatting
    formatted_lines = [
        str(line).replace("\r\n", indent) for line in contents if str(line) != "<br/>"
    ]

    # Join the formatted lines with newlines
    formatted_string = "\n".join(formatted_lines)

    return formatted_string


def sent_text(message):
    token = os.environ["CHAT_TOKEN"]
    chat_id = os.environ["CHAT_ID"]
    url = os.environ["NOTIFICATION_URL"]
    try:
        response = requests.get(url.format(token, chat_id, message), timeout=15)
        response.raise_for_status()
    except Exception as e:
        send_email(f"Exception during notify telegram: {e}")


def crawl():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        print(f"Fetching URL: {os.environ['SOURCE_URL']}")
        result = requests.get(
            os.environ["SOURCE_URL"],
            timeout=30,  # Increased timeout
            headers=headers,
            verify=True  # Explicitly verify SSL
        )
        print(f"Response status code: {result.status_code}")
        result.raise_for_status()
        soup = bs4.BeautifulSoup(result.text, "html.parser")
        items = soup.select("#postContent>a")
        print(f"Found {len(items)} items to process")
        for item in items:
            content = format_content(item.contents)
            pk = md5(content.encode()).hexdigest()
            schedule_repository.insert({
                "pk": pk,
                "data": content
            })
    except requests.exceptions.SSLError as e:
        send_email(f"SSL Error while retrieving water outages info: {e}")
    except requests.exceptions.ConnectionError as e:
        send_email(f"Connection Error while retrieving water outages info: {e}")
    except requests.exceptions.Timeout as e:
        send_email(f"Timeout Error while retrieving water outages info: {e}")
    except Exception as e:
        send_email(f"Exception during retrieving water outages info: {str(e)}")


def send_email(content):
    print(f"Sending email to admin:{content}")
    admin_email = os.environ["ADMIN_EMAIL"]
    client = boto3.client('ses')
    response = client.send_email(
        Source=admin_email,
        Destination={
            'ToAddresses': [
                admin_email
            ],
            'CcAddresses': [],
            'BccAddresses': []
        },
        Message={
            'Subject': {
                'Data': '[Lịch cúp nước] Incident notification',
                'Charset': 'UTF-8'
            },
            'Body': {
                'Html': {
                    'Data': content,
                    'Charset': 'UTF-8'
                }
            }
        },
        ReplyToAddresses=[],
        Tags=[
            {
                'Name': 'string',
                'Value': 'string'
            },
        ]
    )
    print(response)
