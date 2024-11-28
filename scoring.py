import multiprocessing
from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.pydantic_v1 import BaseModel, Field

class InterviewAnswerScorer:
    """A class to score interview answers using a language model.
        structured_llm (object): An instance of a language model with structured output.
    Methods:
        __init__(modelpath: str) -> None:
            Initializes the InterviewAnswerScorer class with a given model path.
        initalize_model(modelpath: str) -> None:
        score_answer(question: str, answer: str) -> dict:"""
    
    class AnswerScore(BaseModel):
        """
        A model representing the score and reasoning for an interview answer.

        Attributes:
            score (int): The score between 0% and 100%.
            reasoning (str): The reasoning for the score.
        """
        score: int = Field(description="The score between 0% and 100%")
        reasoning: str = Field(description="The reasoning for the score")
        
    def __init__(self, modelpath:str) -> None:
        """
        Initializes the InterviewAnswerScorer class with a given model path.

        Args:
            modelpath (str): The file path to the model to be initialized.

        Sets:
            system_prompt (str): A prompt string for scoring interview answers.
        """
        self.system_prompt = (
            f"You are an AI assistant that scores interview answers. "
            f"For each question and answer provided, give a score between 0% and 100% and provide reasoning for the score."
        )
        self.initalize_model(modelpath)

    def initalize_model(self, modelpath:str) -> None:
        """
        Initializes the language model with the specified parameters.

        Args:
            modelpath (str): The path to the model file.

        Returns:
            None
        """
        llm = ChatLlamaCpp(
            temperature=0.5,
            model_path=modelpath,
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
        self.structured_llm = llm.with_structured_output(self.AnswerScore)

    def score_answer(self, question: str, answer: str) -> dict:
        """
        Scores an interview answer based on a given question.

        Args:
            question (str): The interview question.
            answer (str): The interview answer.

        Returns:
            dict: A dictionary containing the score and reasoning.
        """
        messages = [
            ("system", self.system_prompt),
            ("human", f"Question: {question}\nAnswer: {answer}"),
        ]
        response = self.structured_llm.invoke(messages)
        return response

if __name__ == "__main__":

    # Path to your model weights
    local_model = "Mistral-Nemo-Instruct-2407-Q4_K_M.gguf"

    # Initialize the InterviewAnswerScorer
    scorer = InterviewAnswerScorer(local_model)

    # Example usage
    question = "What is polymorphism in OOP?"
    answer = "Polymorphism is the ability of an object to take on many forms."
    result = scorer.score_answer(question, answer)
    print(result)
