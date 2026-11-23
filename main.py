
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

print("================================")
print("       NEXUS AI ACTIVATED")
print("================================")

if not api_key:
    print("ERROR: Groq API key .env file mein nahi mili!")
    exit()

client = Groq(api_key=api_key)

print("Hello! I am Nexus AI.")
print("Type exit to close.")

while True:
    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are Nexus AI, a helpful AI assistant."},
                {"role": "user", "content": question}
            ]
        )

        print("\nNexus AI:", response.choices[0].message.content)

    except Exception as error:
        print("Error:", error)
