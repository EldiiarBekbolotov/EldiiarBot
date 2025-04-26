from groq import Groq
client = Groq(api_key='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')
def ask_groq(prompt):
    chat_completion = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return chat_completion.choices[0].message.content
print("Groq Chatbot (type 'exit' to quit)")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = ask_groq(user_input)
    print("Bot:", response)
