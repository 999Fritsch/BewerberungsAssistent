import csv
import multiprocessing
from langchain_community.chat_models import ChatLlamaCpp
import re

# Path to your model weights
local_model = "Phi-3.5-mini-instruct-IQ4_XS.gguf"

llm = ChatLlamaCpp(  # C++ im Hintergrund statt Ollama
    temperature=0,
    model_path=local_model,
    n_ctx=10000,
    n_gpu_layers=0,
    n_batch=300,  # Adjust based on your system resources
    max_tokens=512,
    n_threads=multiprocessing.cpu_count() - 1,
    repeat_penalty=1.5,
    top_p=0.5,
    verbose=False,
    seed=42
)

# Read the CSV file
questions = []
answers = []

with open('fragen_antworten.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        questions.append(row['Frage'])
        answers.append(row['Antwort'])

# Use ChatLlamaCpp to evaluate the answer
system_prompt = (
    'Du bekommst eine Frage und eine Bewerberantwort und bewertest wie gut die Frage beantwortet wurde. '
    'Du Antwortest stur nur mit einer Prozentzahl. 0 % komplett Falsch bis 100 % alles Richtig'
)

res = []
for question, answer in zip(questions, answers):
    messages = [
        ("system", system_prompt),
        ("human", f'Antwort "{answer}"; Frage "{question}"')
    ]
    #print(messages)
    # for chunk in llm.stream(messages):
    #     print(chunk.content, end="", flush=True)
    # print()  # Print a newline after each evaluation

    context = llm.invoke(messages)

    res = re.findall('(\d{1,3})\s?%', context.content)
    print(f'Antwort "{answer}"; Frage "{question}"')
    print(res)
    #print(context.content)


print(res)