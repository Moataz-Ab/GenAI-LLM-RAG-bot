# GenAI-LLM-RAG-bot

In this work, we use Generative AI LLM modeling techniques to create a project management RAG system tool.
RAG is a coloring system that assigns a color (Red, Amber, or Green) to each project task indicating its progress status.

![](img/app_snapshot.jpg)

After the project data is fed into the tool, the LLM model is prompted to provide project management expert recommendation on how to proceed on the task according to its understanding of the data provided.

![](img/recommendation_snapshot.jpg)

# Methodology

- Utilizing LangChain open source framwork to create the LLM model
- Using OpenAI API as our prompting channel
- The user interface app is created using Flask web frame

# Using the app
- The app simplifies the RAG system into evaluating the task status based on the spent budget and the task deadline
- The initial project data is fed into app in csv format
- The user defines the number of the task and the budget spent on the task to date
- The app returns the RAG status of the task and strategic recommendations on how to proceed based on the budget status and the distance from the deadline
