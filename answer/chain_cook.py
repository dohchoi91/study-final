import os
import platform

import openai
import chromadb
import langchain
import tiktoken

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory


def answer_on_cook(query: str, api_key: str)->any:
  print("======= 시작 ========")

  embedding_function = OpenAIEmbeddings(openai_api_key=api_key)
  
  # client = chromadb.PersistentClient(path="./chroma/cook")
  # vectordb = Chroma(
  #   client=client,
  #   collection_name='cook',
  #   embedding_function=embedding_function
  # )
  vectordb = Chroma(persist_directory="./chroma/cook", embedding_function=embedding_function)
  
  model = ChatOpenAI(temperature=0.0, model_name="gpt-3.5-turbo", openai_api_key=api_key)
  
  memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
  chain = ConversationalRetrievalChain.from_llm(llm = model, retriever=vectordb.as_retriever(), memory=memory)
  tip = "(레시피를 자세하게 설명하고, 썸네일과 비디오링크를 알고 있다면 보여줘)"
  result = chain({"question": query + tip})
  print(result)
  
  
  return result['question'], result['answer']
