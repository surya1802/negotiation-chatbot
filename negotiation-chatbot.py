import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class NegotiationChatbot:
    def __init__(self, product_name, min_price, max_price):
        self.product_name = product_name
        self.min_price = min_price
        self.max_price = max_price
        self.current_price = max_price
        self.conversation_history = []

    def generate_response(self, user_message):
        # Add user message to conversation history
        self.conversation_history.append(f"Customer: {user_message}")

        # Prepare the prompt for the AI model
        prompt = f"""
You are a supplier negotiating the price of {self.product_name}. Your current offer is ${self.current_price}.
The minimum price you can accept is ${self.min_price}, and the maximum price is ${self.max_price}.
Respond to the customer's message and continue the negotiation. Be polite but firm.

Conversation history:
{' '.join(self.conversation_history)}

Supplier:"""

        # Generate response using OpenAI's GPT-3.5
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        ai_response = response.choices[0].text.strip()
        self.conversation_history.append(f"Supplier: {ai_response}")
        return ai_response

    def update_price(self, new_price):
        if self.min_price <= new_price <= self.max_price:
            self.current_price = new_price
            return True
        return False

    def negotiate(self):
        print(f"Welcome! Let's negotiate the price for {self.product_name}.")
        print(f"Our initial offer is ${self.current_price}.")

        while True:
            user_input = input("Your response (or 'quit' to end): ")
            
            if user_input.lower() == 'quit':
                print("Thank you for negotiating. Goodbye!")
                break

            ai_response = self.generate_response(user_input)
            print(f"Supplier: {ai_response}")

            # Simple price update logic (can be improved)
            if "$" in user_input:
                try:
                    proposed_price = float(user_input.split("$")[1].split()[0])
                    if self.update_price(proposed_price):
                        print(f"Price updated to ${self.current_price}")
                    else:
                        print("Proposed price is outside acceptable range.")
                except ValueError:
                    print("Invalid price format. Please use '$X' format.")

if __name__ == "__main__":
    chatbot = NegotiationChatbot("Premium Widget", 80, 120)
    chatbot.negotiate()
