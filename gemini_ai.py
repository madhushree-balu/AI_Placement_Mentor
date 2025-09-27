import os
from typing import Optional
from google import genai
from google.genai import types
import dotenv

dotenv.load_dotenv(".env")

def get_gemini_response(prompt: str,
                        model_name: str = "gemini-1.5-flash",
                        api_key: Optional[str] = None) -> str:
    """
    Get response from Gemini API (via the new google-genai SDK) for a given prompt.
    """
    # Determine and set the API key or client config
    if api_key:
        client = genai.Client(api_key=api_key)
    else:
        env_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not env_key:
            raise ValueError("API key not provided. "
                             "Set GOOGLE_API_KEY / GEMINI_API_KEY or pass api_key parameter.")
        client = genai.Client(api_key=env_key)
    
    # Prepare the request
    # `contents` can be a string, list of strings, or a types.Content / types.UserContent
    contents = prompt  # simplest form: string
    
    # Optionally, you can pass config settings (temperature, max output tokens, etc.)
    # For example:
    config = types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=512,
        # system_instruction etc. if needed
    )
    
    # Call the model
    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=config
    )
    
    return response.text if response.text else ""

class GeminiWrapper:
    def __init__(self, model_name: str = "gemini-1.5-flash", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
        self.gemini = genai.Client(api_key=self.api_key)


    def get_response(self, prompt: str) -> str:
        return get_gemini_response(prompt, model_name=self.model_name, api_key=self.api_key)
    
    def get_tech_question(self, job_description: str, previous_questions: list) -> str:
        prompt = """
Generate me a question to ask a candidate about the job description and these are the previous questions: {previous_questions}.
The output should be structured into a json format, the required format is:
{
    'question': 'question',
    'answer': 'answer',
    topics: []
}
"""
        response = get_gemini_response(prompt, model_name=self.model_name, api_key=self.api_key)
        return response

    def validate_tech_question_answer(self, question: str, answer: str) -> bool:
        prompt = """
Check if the given answer is correct for the following question and give the response in a json format.
Question: {question}
Answer: {answer}
The format you should return is:
{
    'correct': True or False
    'reason': 'reason'
}
"""
        response = get_gemini_response(prompt, model_name=self.model_name, api_key=self.api_key)
        return response