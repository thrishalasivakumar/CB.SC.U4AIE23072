import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

LOG_API = "http://20.207.122.201/evaluation-service/logs"


def Log(stack, level, package, message):

    payload = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    try:

        response = requests.post(
            LOG_API,
            json=payload,
            headers=headers
        )

        return response.status_code

    except Exception as e:

        print("Logging Failed:", str(e))