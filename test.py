from gemini_ai import GeminiWrapper
from roadmap_dataset import data_dict

gemini = GeminiWrapper()
# print(gemini.get_response("hello"))
# print(gemini.get_tech_question("Software Engineer", []))
# print(gemini.validate_tech_question_answer("What is a software engineer?", "Software engineers design, develop, and maintain software applications"))
# print(gemini.validate_tech_question_answer("What is python", "It is a snake"))

plantuml_code = gemini.generate_roadmap("How to create full stack application. I already know python. I want to integrate sqlite, jwt and react", data_dict)
print(plantuml_code)