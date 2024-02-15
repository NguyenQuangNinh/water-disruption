import bs4
import os
import requests
from hashlib import md5

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
    requests.get(
        "https://api.telegram.org/{}/sendMessage?chat_id={}&text={}".format( token, chat_id,
                                                                            message), timeout=15)


def detect_news():
    date_pattern = r'\b\d{2}/\d{2}/\d{4}\b'
    result = requests.get("https://capnuoccholon.com.vn/tin-tuc/tb-tam-ngung-cung-cap-nuoc-quan-5.html", timeout=15)
    soup = bs4.BeautifulSoup(result.text, "html.parser")
    for item in soup.select("#postContent>a"):
        content = format_content(item.contents)
        pk = md5(content.encode()).hexdigest()
        schedule_repository.insert({
            "pk": pk,
            "data": content
        })
