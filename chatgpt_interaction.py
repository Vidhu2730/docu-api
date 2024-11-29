from flask import Flask, jsonify, request
import requests
import json

with open('config.json') as config_file:
    config = json.load(config_file)

OPENAI_API_KEY = config['openai_api_key']
OPENAI_API_URL = config['openai_api_request_url']

headers = {
    'Content-Type': 'application/json',
    'API-Key': OPENAI_API_KEY
}

def ask_openai(user_prompt):
    print(f'user_prompt.........',user_prompt)
    # Define the payload
    payload = {
        "messages": [
            {"role": "system", "content": "Please respond in JSON format. If the user is asking anything on any topic, respond with the structure: {\"searchtopic\": \"topicname\"}."
                                            "If user is asking to summarize the content from a particular confluence page then extract the page id and respond with the structure: {\"summarizepage\": \"pageid\"}. Page id in number, so don't provide this response if page id incorrect."
                                            "For other queries apart from searching, respond with the string not json."
                                            "You are DocuAI, who search and find insights from confluence documents. So, response accordingly if user is just saying hello, hi or something like this."
                                            },
            {"role": "user", "content": user_prompt}
        ]
    }

    # Send the request to the OpenAI API
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
    print(f"response------------",response)
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()


def ask_openai_to_summarize(prompt, data):
    print(f'ask_openai_to_summarize================', data)
    # Define the payload
    combined_content = f"data content is : {data}\""
    payload = {
  "messages": [
            {"role": "system", "content":   "Focus on data content from user role. It will be in json format but need to summarize it."
                                            "Your name DocuAI. Your job is to Chat and search right page and content on confluence"
                                            "If user is just saying hello,how are or something like this, introduce yourself. Don't do this user is asking for some relevant content."
                                            "This is a response to end user. Summarize the data from 'data content'"
                                            "If there is any search result, then mandatorily list all UI pages from the data (not rest api). Append https://docuaihackathonpoc.atlassian.net/wiki/ for fully defined UI page if exists."
                                            "Add html tags in the result"
                                            "If user is searching something but no result in the confluence, then say no result found in confluence page after saying what exactly is. For example, If user asking you to elaborate on topic Spring boot which is not there in user content, the explain in 2 lines what is spring boot and then say I don't have any result on this topic from Confluence pages. Same apply for any topic without content in user input"
                                            "No introduction required for every response"
                                            
                                            },
            {"role": "user", "content": combined_content}
    ],
    "temperature": 0.7
}

    # Send the request to the OpenAI API
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
    print(response.json())
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()