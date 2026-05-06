import requests
import os

from dotenv import load_dotenv
from logging_middleware.logger import Log

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

BASE_URL = "http://20.207.122.201/evaluation-service"

headers = { "Authorization": f"Bearer {ACCESS_TOKEN}" }


def get_depots():

    Log(
        "backend",
        "info",
        "service",
        "Fetching depots data"
    )

    response = requests.get( f"{BASE_URL}/depots", headers=headers )
    return response.json()["depots"]


def get_vehicles():

    Log(
        "backend",
        "info",
        "service",
        "Fetching vehicles data"
    )

    response = requests.get( f"{BASE_URL}/vehicles", headers=headers )

    return response.json()["vehicles"]