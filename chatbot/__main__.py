import os
import sys
import rich
from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values()

if len(sys.argv) > 1:
    try: 
        with open(sys.argv[1]) as file:
                system_content = file.read()

                history = [
                    {
                        "role": "system",
                        "content": system_content
                    }
                ]
    except FileNotFoundError:
        print("Please use a valid text file.")
        sys.exit(1)
else:

    history = [
        {
            "role": "system",
            "content": "Be helpful."
        }
    ]

client = OpenAI(
    api_key=config.get("OPENAI_API_KEY")
)

def chat_me(client):

    content = input("> ")
    history.append({"role": "user", "content": content})

    chat_completion = client.chat.completions.create(

        messages = history,
        model="gpt-4-turbo"

    )

    message = chat_completion.choices[0].message
    print(chat_completion.choices[0].message.content)
    return {"role": message.role, "content": message.content}

    
def get_models(client):
    print(len(list(client.models.list())))
    for model in client.models.list():
        rich.print(model)

def update_history():    
    history.append(chat_me(client))
    # rich.print(history)
    
while True:
    update_history()
