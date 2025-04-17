from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# Chat history
chat_history_ids = None
step = 0

print("Start chatting with the bot (type 'exit' to stop)")

while True:
    user_input = input(">> User: ")
    if user_input.lower() == "exit":
        break

    # Encode user input + chat history
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # If chat history exists, concatenate it with the new input
    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
    else:
        bot_input_ids = new_input_ids

    # Ensure the length of the tensor doesn't exceed the model's max input length
    max_length = 1024  # GPT-2 model max length is typically 1024 tokens
    bot_input_ids = bot_input_ids[:, -max_length:]  # Slice to keep the last 1024 tokens

    # Create an attention mask for the input
    attention_mask = torch.ones(bot_input_ids.shape, device=bot_input_ids.device)

    # Generate response
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id, attention_mask=attention_mask)

    # Decode the response from the model
    bot_output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Check if the model is repeating itself and handle it
    if bot_output == user_input:
        bot_output = "I'm not sure about that. Could you clarify?"

    print(f"🤖 Bot: {bot_output}")
    step += 1
