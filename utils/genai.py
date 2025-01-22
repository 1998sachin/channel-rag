import os
import google.generativeai as genai
from typing import Generator

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def chat_stream(messages: list, max_tokens: int = 1000, temperature: float = 0.1) -> Generator[str, None, None]:
    """
    Stream responses from Gemini model for chat interactions.
    
    Args:
        messages: List of message dictionaries with role and content
        max_tokens: Maximum number of tokens in the response (default 1000)
        temperature: Controls randomness in responses (default 0.1)
        
    Yields:
        Generated text chunks from the model response
    """
    # Configure the API
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Initialize the model and chat
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    chat = model.start_chat(history=[
        {"role": msg["role"], "parts": msg["content"]} 
        for msg in messages[:-1]  # Convert all but last message to chat history
    ])
    
    # Send the last message and stream response
    response = chat.send_message(
        messages[-1]["content"],
        generation_config=genai.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        ),
        stream=True
    )
    
    # Yield chunks of generated text
    for chunk in response:
        if chunk.text:
            yield chunk.text
