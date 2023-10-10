# GenAI-LLM-RAG-bot

⌛ Work in progress... ⌛

In this work, we use Generative AI LLM modeling techniques to create a project management RAG system tool.

# Methodology

- Utilizing LangChain open source framwork to create the LLM model
- Using OpenAI API as our prompting channel
- The user interface app is created using Flask web frame

# Using the app
- The app simplifies the RAG system into evaluating the task status based on the spent budget and the task deadline
- The initial project data is fed into app in csv format
- The user defines the number of the task and the budget spent on the task to date
- The app returns the RAG status of the task and strategic recommendations on how to proceed based on the budget status and the distance from the deadline
