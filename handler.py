import json
import service as service


def crawl(event, context):
    service.crawl()


def notify(event, context):
    print(f"Received event: {event}")
    sub_event = [json.loads(item['body']) for item in event['Records']]
    for record in sub_event:
        print(f"Processing record = {record}")
        if record["eventName"] == "INSERT" or record["eventName"] == "MODIFY":
            service.sent_text(record["dynamodb"]["NewImage"]["data"]["S"])


if __name__ == "__main__":
    service.crawl()