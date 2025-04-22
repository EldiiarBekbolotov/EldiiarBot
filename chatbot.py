from transformers import pipeline

# Load the text-generation pipeline with the specified model
text_generator = pipeline(task="text-generation", model="Qwen/Qwen2.5-1.5B")

# Function to simulate a conversation
def chat_with_bot():
    print("Bot is ready! Type 'exit' to end the conversation.")
    
    while True:
        # Get user input
        user_input = input("You: ")
        # Exit condition
        if user_input.lower() == "exit":
            print("Bot: Goodbye!")
            break
        
        # Generate a response using the model
        response = text_generator(user_input, truncation=True, max_new_tokens=50)
        
        # Print the bot's reply
        print("Bot:", response[0]['generated_text'])

# Start the chat
if __name__ == "__main__":
    chat_with_bot()


"""# Initialize the text-generation pipeline
text_generator = pipeline(task="text-generation", model="Qwen/Qwen2.5-1.5B")

# Generate text with explicit truncation and appropriate length controls
response = text_generator(
    "the secret to baking a really good cake is ",
    max_new_tokens=50,  # Use this to control new token generation
    truncation=True     # Explicitly enable truncation
)

# Print the generated text
print(response[0]['generated_text'])"""