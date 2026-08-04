from langchain_community.llms import Ollama

# Initialize the local Llama 3 model
llm = Ollama(
    model="llama3",
    temperature=0.2
)

if __name__ == "__main__":
    question = "What is the profit in May 2023?"

    response = llm.invoke(question)

    print("=" * 50)
    print(response)
