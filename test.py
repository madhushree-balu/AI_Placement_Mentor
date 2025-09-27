from gemini_ai import GeminiWrapper

gemini = GeminiWrapper()
print(gemini.get_response("hello"))
print(gemini.get_tech_question("Software Engineer", []))
print(gemini.validate_tech_question_answer("What is a software engineer?", "Software engineers design, develop, and maintain software applications"))
print(gemini.validate_tech_question_answer("What is python", "It is a snake"))
