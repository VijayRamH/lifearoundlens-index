################################################################
# CLI program for querying document via LLM
# Uses ChatGPT for LLM and PineCone for vector database
################################################################ 
from doc_query import *

#----------------------------------------------------
# insert_or_fetch_embeddings()
# Given an index and chunks of file data this method
# checks for the existance of that index (or) creates
# it first. Then it adds the embeddings inside it.
#
# dependencies - expects .env file with openai and 
# pinecone keys available in the current directory.
#----------------------------------------------------
def insert_or_fetch_embeddings(index_name, chunks):
    import pinecone
    from langchain.vectorstores import Pinecone
    from langchain.embeddings import OpenAIEmbeddings
    import os
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv(), override=True)
    embeddings = OpenAIEmbeddings()

    pinecone.init(
        api_key     =   os.environ.get('PINECONE_API_KEY'),
        environment =   os.environ.get('PINECONE_ENV')
    )

    if index_name in pinecone.list_indexes():
        print(f"Index {index_name} already exists in pinecone.")
        vector_store = Pinecone.from_existing_index(index_name, embeddings)
    else:
        print(f"Creating index {index_name} ...")
        pinecone.create_index(index_name, dimension=1536, metric='cosine')
        vector_store = Pinecone.from_documents(chunks, embeddings, index_name=index_name)

    print("Loaded embeddings ...")
    return vector_store            

#----------------------------------------------------
# get_answer()
# Given a vector store with content embeddings and a
# question it returns the answer for that question.
# This method does not store context with respect to
# previously asked questions and their answers.
#----------------------------------------------------
def get_answer(vector_store, question):
    from langchain.chains import RetrievalQA
    from langchain.chat_models import ChatOpenAI

    llm         =   ChatOpenAI(model='gpt-3.5-turbo', temperature=0.7)
    retriever   =   vector_store.as_retriever(search_type='similarity', search_kwargs={'k':3})
    chain       =   RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever)
    answer      =   chain.run(question)

    return answer

#--------------------------------------------------------
# get_answers_with_memory()
# Given a vector store with content embeddings and a
# question it returns the answer for that question.
# This method references earlier context while answering
# new questions.
#--------------------------------------------------------
def get_answers_with_memory(vector_store, question, chat_history):
    from langchain.chains import ConversationalRetrievalChain
    from langchain.chat_models import ChatOpenAI

    llm         =   ChatOpenAI(model='gpt-3.5-turbo', temperature=0.7)
    retriever   =   vector_store.as_retriever(search_type='similarity', search_kwargs={'k':3})
    chain       =   ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)
    result      =   chain.run({'question':question, 'chat_history':chat_history})

    #append answer to chat_history
    chat_history.append((question, result))

    return result, chat_history

#--------------------------------------------------------
# main() - a simple interactive shell to ask repeated 
# queries on the document
#--------------------------------------------------------
document    =   input("Enter the document to read (as full path) -> ")
docQuery    =   DocQuery(document)
vs          =   insert_or_fetch_embeddings("query-index", docQuery.getDocumentChunks())

import time
chat_history =[]
i = 1
print("Type 'exit' to quit this interface ...")

while True:
    query = input(f'Question #{i} -> ')
    i=i+1
    if query.lower() in ['exit']:
        print("Exiting ...")
        time.sleep(2)
        break
    ans, chat_history = get_answers_with_memory(vs, query,chat_history)
    print(f"Answer -> {ans}")
    print(f'\n {"-" * 50} \n')