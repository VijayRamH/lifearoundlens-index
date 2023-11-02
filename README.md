# Repo - query_doc_llm
Code repo to demo the power of LLM's using Langchain framework. This example is based on learnings from "Hands-On Applications with LangChain, Pinecone, and OpenAI. Build Web Apps with Streamlit" - Udemy Course by Andrei Dumitrescu.

# What it does
Provides a simple command line tool to query a document which can either have a .pdf (or) .docx extension. The query is done via an interactive CLI program through which you can load a document and ask it questions. Type exit to come out of the CLI prompt.

# How it does it
Using Langchain and Pinecone (vector store) libraries, this project loads up a given document (PDF/DOCX in this example) and converts it into chunks. Then it embeds these chunks within a pine cone index and allows querying of the same via LLM.

# Does it have memory?
Yes it does have memory for that session as questions and answers asked earlier (in that session) are referrenced while answering further queries.

# What can be extended here?
You can enhance it to add support for various other documents - TO BE DONE - Support for additional LLMs.

# What are the pre-requisites?
OpenAI key
Pinecone keys
Install python requirements.txt modules
