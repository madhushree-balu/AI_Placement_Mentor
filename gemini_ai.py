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
