import json
import uuid

import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

CLIENT_ID = st.secrets["CLIENT_ID"]
SECRET = st.secrets["SECRET"]

messages = []
data = {
    "model": "GigaChat",
    "messages": [],
}


def check_credentials(username, password):
    valid_users = {
        "acidsugarx": "123456",
        "ruslan": "123456"
    }
    return valid_users.get(username) == password


def get_access_token() -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
    }
    payload = {"scope": "GIGACHAT_API_PERS"}
    res = requests.post(
        url=url,
        headers=headers,
        auth=HTTPBasicAuth(CLIENT_ID, SECRET),
        data=payload,
        verify=False,
    )
    access_token = res.json()["access_token"]
    return access_token


def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    messages.append({"role": "user", "content": msg})
    data["messages"].append(messages[-1])
    payload = json.dumps(data)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)

    try:
        response_json = response.json()
        print(response_json)  # Print the response for debugging
        assistant_message = response_json["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": assistant_message})
        data["messages"].append(messages[-1])
        return assistant_message
    except KeyError:
        print(f"Unexpected response structure: {response_json}")
        return "An error occurred. Please try again."


