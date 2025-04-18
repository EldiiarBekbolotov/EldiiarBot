
from llama_cpp import Llama

llm = Llama(model_path="mistral.gguf", n_ctx=512)

print("🧠 Local Chat — type 'exit' to quit.\n")
history = []

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        break

    # You can keep a simple chat format
    prompt = f"User: {user_input}\nAssistant:"
    
    output = llm(prompt, max_tokens=200, stop=["User:", "You:"], echo=False)
    response = output["choices"][0]["text"].strip()
    print(f"Bot: {response}\n")
