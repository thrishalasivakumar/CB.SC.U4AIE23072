import requests
import heapq
import os

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

URL = "http://20.207.122.201/evaluation-service/notifications"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# Priority weights
priority_weights = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

response = requests.get(
    URL,
    headers=headers
)

data = response.json()["notifications"]

heap = []

for notification in data:

    notification_type = notification["Type"]

    timestamp = datetime.strptime(
        notification["Timestamp"],
        "%Y-%m-%d %H:%M:%S"
    )

    weight = priority_weights[notification_type]

    # Higher weight + recent timestamp
    score = (
        weight,
        timestamp
    )

    heapq.heappush(heap, (
        score,
        notification
    ))

    # Maintain only top 10
    if len(heap) > 10:
        heapq.heappop(heap)

top_notifications = sorted(
    heap,
    reverse=True
)

print("\nTOP 10 PRIORITY NOTIFICATIONS\n")

for item in top_notifications:

    notification = item[1]

    print("=" * 50)
    print(f"Type      : {notification['Type']}")
    print(f"Message   : {notification['Message']}")
    print(f"Timestamp : {notification['Timestamp']}")
    print("=" * 50)