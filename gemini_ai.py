import os
from typing import Optional
from google import genai
from google.genai import types
import dotenv

dotenv.load_dotenv(".env")


class GeminiWrapper:
    def __init__(self, model_name: str = "gemini-2.0-flash-001", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
        if self.api_key is None:
            env_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            self.api_key = env_key
        self.gemini = genai.Client(api_key=self.api_key)


    def get_response(self, prompt: str) -> str:
        response = self.gemini.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text
    
    def get_tech_question(self, job_description: str, previous_questions: list) -> str:
        prompt = f"""
Generate me a question to ask a candidate about the job description and these are the previous questions: {previous_questions}.
The output should be structured into a json format, the required format is:
{{
    'question': 'question',
    'answer': 'answer',
    'topics': []
}}
"""
        response = self.get_response(prompt)
        return response

    def validate_tech_question_answer(self, question: str, answer: str) -> str:
        prompt = f"""
Check if the given answer is correct for the following question and give the response in a json format.
Question: {question}
Answer: {answer}
The format you should return is:
{{
    'correct': True or False,
    'reason': 'reason'
}}
"""
        response = self.get_response(prompt)
        return response

    def generate_roadmap(self, description: str, data_dict: dict = None) -> str:
        # Base examples for few-shot prompting if no data_dict provided
        examples = ""
        
        if data_dict and "data" in data_dict:
            # Use provided examples from data_dict
            examples_list = data_dict["data"][:3]  # Use first 3 examples to avoid token limits
            for i, example in enumerate(examples_list, 1):
                examples += f"""
Example {i}:
Human: {example['prompt']}
Assistant: {example['response']}

"""
        
        prompt = f"""You are an expert at creating comprehensive learning roadmaps using PlantUML mind maps. 

{examples}Based on the examples above, generate a detailed PlantUML mind map roadmap for the following description:

{description}

Requirements:
1. Use the @startmindmap and @endmindmap tags
2. Include a descriptive title
3. Use styling with color-coded categories (beginner, intermediate, advanced, etc.)
4. Organize content hierarchically with proper indentation
5. Include relevant subtopics and detailed learning points
6. Add a legend explaining the color coding
7. Follow the same structure and depth as the examples
8. The output should be ONLY the PlantUML code, nothing else.
"""
        
        response = self.get_response(prompt)
        return response.strip('```').strip('plantuml')
