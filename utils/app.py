import itertools
import gradio as gr
import requests
import os
from gradio.themes.utils import sizes


def respond(message, history):

    if len(message.strip()) == 0:
        return "ERROR the question should not be empty"

    local_token = os.getenv('DATABRICKS_TOKEN')
    local_endpoint = os.getenv('API_ENDPOINT')

    if local_token is None or local_endpoint is None:
        return "ERROR missing env variables"

    # Add your API token to the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {local_token}'
    }

    #prompt = list(itertools.chain.from_iterable(history))
    #prompt.append(message)
    #q = {"inputs": [prompt]}
    q = {"inputs": [message]}
    try:
        response = requests.post(
            local_endpoint, json=q, headers=headers, timeout=100)
        response_data = response.json()
        #print(response_data)
        response_data=response_data["predictions"][0]
        #print(response_data)

    except Exception as error:
        response_data = f"ERROR status_code: {type(error).__name__}"
        # + str(response.status_code) + " response:" + response.text

    # print(response.json())
    return response_data


theme = gr.themes.Soft(
    text_size=sizes.text_sm,radius_size=sizes.radius_sm, spacing_size=sizes.spacing_sm,
)


demo = gr.ChatInterface(
    respond,
    chatbot=gr.Chatbot(show_label=False, container=False, show_copy_button=True, bubble_full_width=True),
    textbox=gr.Textbox(placeholder="Ask me a question",
                       container=False, scale=7),
    title="BCF RAG demo - Chat with your BCFing Expert",
    description="This chatbot uses RAG based on public information found on bcf.com.au.",
    examples=[["What is a good family tent?"],
              ["What basics do I need to go camping?"],
              ["Does BCF sell fridges?"],
              ["How do I catch a snapper?"],],
    cache_examples=False,
    theme=theme,
    retry_btn=None,
    undo_btn=None,
    clear_btn="Clear",
)

if __name__ == "__main__":
    demo.launch()