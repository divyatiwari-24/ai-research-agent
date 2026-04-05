from agents import multi_agent_system
import time
if __name__ == "__main__":
    query = input("Enter your question: ")
    time.sleep(10)  
    result = multi_agent_system(query)

    print("\nOUTPUT:\n")
    print(result)