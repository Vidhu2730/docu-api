from flask import Blueprint, Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import json

with open('config.json') as config_file:
    config = json.load(config_file)

USERNAME = config['user_name']
API_TOKEN = config['confluence_api_key']

confluence_bp = Blueprint('confluence', __name__)

def get_confluence_page(page_id):
    url = f'https://docuaihackathonpoc.atlassian.net/wiki/rest/api/content/{page_id}?expand=body.storage'

    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

    if response.status_code == 200:
        data = response.json()
        body_storage_value = data['body']['storage']['value']

        # Remove HTML tags and get plain text
        soup = BeautifulSoup(body_storage_value, 'html.parser')
        plain_text = soup.get_text(separator="\n").strip()  # Get text without HTML tags
        
        return jsonify({"body_storage_value": plain_text})
    else:
        return jsonify({"error": "Failed to retrieve the page", "status_code": response.status_code}), response.status_code

def search_confluence(search_query):

    search_url = f'https://docuaihackathonpoc.atlassian.net/wiki/rest/api/search'
    cql_query = f'text~"{search_query}"'
    params = {'cql': cql_query}

    response = requests.get(search_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN), params=params)
    return response.text



@confluence_bp.route('/confluence/page/<page_id>', methods=['GET'])
def get_confluence_page_from_id(page_id):
    url = f'https://docuaihackathonpoc.atlassian.net/wiki/rest/api/content/{page_id}?expand=body.storage'

    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

    if response.status_code == 200:
        data = response.json()
        body_storage_value = data['body']['storage']['value']

        # Remove HTML tags and get plain text
        soup = BeautifulSoup(body_storage_value, 'html.parser')
        plain_text = soup.get_text(separator="\n").strip()  # Get text without HTML tags
        
        return jsonify({"body_storage_value": plain_text})
    else:
        return jsonify({"error": "Failed to retrieve the page", "status_code": response.status_code}), response.status_code

@confluence_bp.route('/confluence/search', methods=['GET'])
def search_confluence_page():
    print('Helloooooooo')
    search_term = request.args.get('query')
    if not search_term:
        return jsonify({"error": "Query parameter 'query' is required"}), 400

    search_url = f'https://docuaihackathonpoc.atlassian.net/wiki/rest/api/search'
    cql_query = f'text~"{search_term}"'
    params = {'cql': cql_query}

    response = requests.get(search_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN), params=params)
    print(response)
    if response.status_code == 200:
        results = response.json()
        return jsonify({"results": results})
    else:
        return jsonify({"error": "Failed to perform search", "status_code": response.status_code}), response.status_code