from chatgpt_interaction import ask_openai, ask_openai_to_summarize
from confluence_interaction import get_confluence_page, search_confluence
import json

def handle_interaction(original_user_prompt):
    openai_response = ask_openai(original_user_prompt)
    print(openai_response)
    
    content_str = openai_response["choices"][0]["message"]["content"]
    
    
    response = ''
    if "searchtopic" in content_str:
        parsed_content = json.loads(content_str)
        searchtopic = parsed_content["searchtopic"]
        response = search_confluence(searchtopic)
    elif "summarizepage" in content_str:
        print('Summarizing')
        parsed_content = json.loads(content_str)
        pageid = parsed_content["summarizepage"]
        response = get_confluence_page(pageid)


    if not response:
        response = content_str

    final_response = ask_openai_to_summarize(original_user_prompt, response)

    return final_response