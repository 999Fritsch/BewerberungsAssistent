import multiprocessing
from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.pydantic_v1 import BaseModel, Field
from time import time

class InterviewQuestion(BaseModel):
    """
    A model representing an interview question.

    Attributes:
        question (str): An interview question.
    """
    question: str = Field(description="An interview question")

def generate_interview_questions(skill, N, structured_llm):
    """
    Generates a list of technical interview questions based on a given skill.

    Args:
        skill (str): A skill for which to generate questions.
        N (int): The number of questions to generate.
        structured_llm (object): An instance of a language model with an `invoke` method to generate questions.

    Returns:
        list of str: A list of generated interview questions.

    Example:
        skill = "Python"
        N = 5
        structured_llm = SomeLanguageModel()
        questions = generate_interview_questions(skill, N, structured_llm)
    """
    system_prompt = (
        f"You are an AI assistant that generates a short and concise technical question based on a given skill. "
        f"For each skill provided, generate relevant and challenging technical question that have only one correct answer. "
        f"Provide only the question, not the answer."
    )
    messages = [
        ("system", system_prompt),
        ("human", f"Skill: {skill}"),
    ]
    questions = []
    for _ in range(N):
        question = structured_llm.invoke(messages)
        questions.append(question)
    return questions

if __name__ == "__main__":

    # Path to your model weights
    local_model = "Mistral-Nemo-Instruct-2407-Q4_K_M.gguf"

    llm = ChatLlamaCpp(
        temperature=0.5,
        model_path=local_model,
        n_ctx=10000,
        #n_gpu_layers=0,
        n_batch=512,  # Adjust based on your system resources
        max_tokens=512,
        n_threads=multiprocessing.cpu_count() - 1,
        repeat_penalty=1.5,
        top_p=0.5,
        verbose=False,
        seed=42
    )
    structured_llm = llm.with_structured_output(InterviewQuestion)

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
    skill = skills[0]
    N = 5
    start_time = time()
    questions = generate_interview_questions(skill, N, structured_llm)
    end_time = time()
    print(f"Time taken: {end_time - start_time} seconds")
    print(questions)