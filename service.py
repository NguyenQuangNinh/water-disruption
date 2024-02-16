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
        result = requests.get(os.environ["SOURCE_URL"], timeout=15)
        result.raise_for_status()
        soup = bs4.BeautifulSoup(result.text, "html.parser")
        for item in soup.select("#postContent>a"):
            content = format_content(item.contents)
            pk = md5(content.encode()).hexdigest()
            schedule_repository.insert({
                "pk": pk,
                "data": content
            })
    except Exception as e:
        send_email(f"Exception during retrieving water outages info: {e}")


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
