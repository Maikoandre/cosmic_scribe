from src.core.agent import agent

while True:
    user_input = input("You: ")
    response = agent.run(user_input)
    print(f"Agent: {response}")