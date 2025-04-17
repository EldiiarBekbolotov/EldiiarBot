from transformers import pipeline

chatbot = pipeline("conversational", model="microsoft/DialoGPT-small")
response = chatbot("Hello, how are you?")[0]
print("🤖 Bot:", response["generated_responses"][0])
