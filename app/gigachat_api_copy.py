import json
import uuid

import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

from utills import get_file_id

CLIENT_ID = st.secrets["CLIENT_ID"]
SECRET = st.secrets["SECRET"]

messages = []
data = {
        "model": "GigaChat-Pro",
        "messages": [

        ],
    }


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
    data["messages"].append([messages[-1]])
    payload = json.dumps(data)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    messages.append({"role": "assistant", "content": response.json()["choices"][0]["message"]["content"]})
    data["messages"].append([messages[-1]])
    return response.json()["choices"][0]["message"]["content"]
