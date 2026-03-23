from dotenv import load_dotenv


load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage



model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

print("Press 1 for Active mode")
print("Press 0 for fun mode")

choice = int(input("Enter your choice: "))

if choice == 1:
    mode = "active"
elif choice == 0:   
    mode = "fun"

messages = [
    SystemMessage(content=mode)
]  # List to store the conversation history

print("--- Type your prompt ---")
while True:
    
    prompt = input("you : ")
    messages.append(HumanMessage(content=prompt))  # Add user prompt to the conversation history
    if prompt == "0":
        break
    response = model.invoke(messages)  # Pass the entire conversation history to the model
    messages.append(AIMessage(content=response.content))  # Add model response to the conversation history
    print("Gpt :",response.content) 