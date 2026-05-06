import requests
import os
from dotenv import load_dotenv


TOKEN = os.getenv("FULL_TOKEN")

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

url = "http://20.207.122.201/evaluation-service/depots"

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)