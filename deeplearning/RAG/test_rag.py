import torch
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate


from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI, OpenAIEmbeddings




class RAG:
    def __init__(self, path):
        self.loader = PyMuPDFLoader(path)
        self.device = torch.device("cuda" if torch.backends.mps.is_available() else "cpu")
        
        
        docs = self.loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=50
        )
        split_documents = text_splitter.split_documents(docs)

        embedding_model = HuggingFaceEmbeddings(
            model_name="dragonkue/BGE-m3-ko",
            model_kwargs={'device': self.device},
            encode_kwargs={'normalize_embeddings': True},
        )

        vectorstore = FAISS.from_documents(
            documents=split_documents,
            embedding=embedding_model
        )

        retriever = vectorstore.as_retriever()


        prompt = PromptTemplate.from_template(
            """You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If the user asks for a simple answer, summarize the key points.
        If the question is unrelated to the context in the regulations, respond with "관련 정보를 찾을 수 없습니다."
        Answer in Korean.

        #Context: 
        {context}

        #Question:
        {question}

        #Answer:"""
        )


        # llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
        llm = OllamaLLM(model="gemma3:4b")

        self.chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        
        
    def setup(self):
        pass
    
    

    def get_answer(self, question):
        
        
        return self.chain.invoke(question)
    
if __name__ == '__main__':
    rag = RAG("deeplearning\RAG\datasets\manual.pdf")
    print(rag.get_answer("박사과정의 월급은?"))