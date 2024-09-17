import os
import google.generativeai as genai
import tiktoken

def configure_genai():
    # Fetch the API key from environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables")

    # Configure the SDK with your API key
    genai.configure(api_key=api_key)

    # Define the configuration for the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Initialize the model with the specified configuration
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        # You can adjust safety settings here if needed
        # safety_settings = {...}
    )
    return model

def generate_response(model, input_text, history):
    # Start a chat session with the provided history
    chat_session = model.start_chat(history=history)

    # Send a message to the chat session and get the response
    response = chat_session.send_message(input_text)

    # Update history with the new input and response
    updated_history = history + [
        {
            "role": "user",
            "parts": [input_text],
        },
        {
            "role": "model",
            "parts": [response.text],
        },
    ]

    # Return the response text and the updated history
    return response.text, updated_history

def write_email(email_type, user_input, received_message=None):
    model = configure_genai()

    if email_type == "new":
        # New email history with a detailed prompt
        history = [
            {
                "role": "user",
                "parts": ["I want to write a new email.\n"],
            },
            {
                "role": "model",
                "parts": [
                    "Sure, what would you like to say in your email? Please provide any necessary details such as the subject and the main content.\n"
                ],
            },
        ]
        response, updated_history = generate_response(model, user_input, history)

    elif email_type == "reply":
        if not received_message:
            raise ValueError("Received message is required for reply emails")
        
        # Reply email history with a detailed prompt
        history = [
            {
                "role": "user",
                "parts": [
                    f"I received this message:\n{received_message}\n",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Okay, what would you like to reply? Please provide your response including any necessary details or follow-up questions.\n"
                ],
            },
        ]
        response, updated_history = generate_response(model, user_input, history)
    
    else:
        raise ValueError("Invalid email type. Must be 'new' or 'reply'.")

    return response, updated_history

def count_tokens(text, model_name="gemini-1.5-flash"):
    # Use tiktoken or another tokenizer to count tokens
    # This is an example with a placeholder tokenizer
    encoding = tiktoken.get_encoding("gpt2")  # Replace with the appropriate encoding for the model
    tokens = encoding.encode(text)
    return len(tokens)

# Example usage
try:
    # New email example
    new_email_input = "Hi team, I wanted to remind you about the meeting tomorrow at 10 AM."
    new_email_response, new_email_history = write_email("new", new_email_input)
    print("New Email Response:")
    print(new_email_response)
    print("Updated History:")
    print(new_email_history)

    # Count tokens in the new email response
    token_count = count_tokens(new_email_response)
    print(f"\nToken Count for New Email Response: {token_count}")

    # Reply email example
    received_message = "Can you send me the report by the end of the day?"
    reply_email_input = "Sure, I will send it by 5 PM."
    reply_email_response, reply_email_history = write_email("reply", reply_email_input, received_message)
    print("\nReply Email Response:")
    print(reply_email_response)
    print("Updated History:")
    print(reply_email_history)

    # Count tokens in the reply email response
    token_count = count_tokens(reply_email_response)
    print(f"\nToken Count for Reply Email Response: {token_count}")

except Exception as e:
    print(f"An error occurred: {e}")
