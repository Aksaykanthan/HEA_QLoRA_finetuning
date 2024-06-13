import requests
import json 


url = 'http://localhost:11434/api/chat'


def llama3(prompt):
    data = {
        "model" : "llama3",
        "messages":[
            {
                "role":"user",
                "content":prompt
            }
        ],
        "stream" : False,
    }
    headers = {
        "Content-Type": "application/json"
    }

    response  = requests.post(url,headers=headers,json=data)
    if 'error' in response.json():
        return 'Error'
    
    return response.json()['message']['content']




# response = llama3("hi")
# print(response)