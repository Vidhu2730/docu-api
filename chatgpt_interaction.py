from flask import Flask, jsonify, request
import requests
import json

with open('config.json') as config_file:
    config = json.load(config_file)

OPENAI_API_KEY = config['openai_api_key']
OPENAI_API_URL = config['openai_api_request_url']

def ask_openai(user_prompt):

    # Define the payload
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Please respond in JSON format. If the user is asking to search for content, respond with the structure: {\"searchtopic\": \"topicname\"}. For other queries, respond with the appropriate JSON structure."},
            {"role": "user", "content": user_prompt}
        ]
    }

    # Set up the headers
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Send the request to the OpenAI API
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, verify=False)
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()


def ask_openai_to_summarize(data):

    # Define the payload
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "This is a response to end user. Summarize the data. Mandatorily list all UI pages from the data (not rest api). Append https://docuaihackathonpoc.atlassian.net/wiki/ for fully defined UI page."},
            {"role": "user", "content": data}
        ]
    }

    # Set up the headers
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Send the request to the OpenAI API
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, verify=False)
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()