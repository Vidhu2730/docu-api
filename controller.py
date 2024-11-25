from chatgpt_interaction import ask_openai, ask_openai_to_summarize
from confluence_interaction import get_confluence_page, search_confluence
import json

def handle_interaction(original_user_prompt):
    openai_response = ask_openai(original_user_prompt)
    print(openai_response)
    content_str = openai_response["choices"][0]["message"]["content"]
    parsed_content = json.loads(content_str)
    searchtopic = parsed_content["searchtopic"]

    confluenceresponse = search_confluence(searchtopic)
    final_response = ask_openai_to_summarize(confluenceresponse)
    return final_response