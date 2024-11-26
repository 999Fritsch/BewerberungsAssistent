import multiprocessing
from langchain_community.chat_models import ChatLlamaCpp

# Path to your model weights
local_model = "Phi-3.5-mini-instruct-IQ4_XS.gguf"

llm = ChatLlamaCpp(
    temperature=0.5,
    model_path=local_model,
    n_ctx=10000,
    n_gpu_layers=0,
    n_batch=300,  # Adjust based on your system resources
    max_tokens=512,
    n_threads=multiprocessing.cpu_count() - 1,
    repeat_penalty=1.5,
    top_p=0.5,
    verbose=False,
)

def generate_interview_questions(skills, N):
    skills_str = ', '.join(skills)
    system_prompt = (
        f"You are an AI assistant that generates {N} short and concise technical questions based on a given skill set. "
        f"For each skill provided, generate relevant and challenging technical questions that have only one correct answer. "
        f"Provide exactly {N} questions. Provide only the questions, not the answers. return them in a json format like this: "
        "{'questions': ['question1', 'question2', 'question3', 'question4', 'question5']}"
    )
    messages = [
        ("system", system_prompt),
        ("human", f"Skill set: {skills_str}"),
    ]
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)

# Example usage
skills = [
    "IT Architecture Planning, Experte",
    "IT Architecture Design, Experte",
    "Network Architecture, Experte",
    "GBit Technologies, Fortgeschritten",
    "TBit Technologies, Fortgeschritten",
    "Gateways, Fortgeschritten",
    "IT Security, Experte",
    "Strategic Product Development, Experte",
    "German Language Proficiency, Experte"
]
N = 5
generate_interview_questions(skills, N)