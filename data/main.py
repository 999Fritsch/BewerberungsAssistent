# terminal install ollama
# terminal ollama pull llama3.2
# pip install ollama

# ollama run llama3.2:1b

import ollama

response = ollama.chat(
    model='llama3.2:1b',
    messages=[
        {
            'role': 'user',
            'content': 'What do you think about ChatGPT?'
        },
    ]
)

print(response)