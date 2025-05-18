import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Get the key
api_key = os.getenv("OPENAI_API_KEY")

# Validate the key
if not api_key:
    raise EnvironmentError("❌ OPENAI_API_KEY not found in environment. Please check your .env file or export the variable.")

print("✅ API key loaded successfully.")

client = OpenAI(api_key=api_key)
model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
# Function to call the LLM
def call_llm(prompt, model=model_name):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content

