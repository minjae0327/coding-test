import torch

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


from unstructured.partition.pdf import partition_pdf
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI, OpenAIEmbeddings




class RAG:
    def __init__(self, path):
        # self.device = torch.device("cuda" if torch.backends.mps.is_available() else "cpu")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        elements = partition_pdf(
            filename=path,
            strategy="hi_res",
            infer_table_structure=True,
            model_name="yolox"
        )

        markdown_text = ""

        for el in elements:
            if "unstructed.documents.elements.Title" in str(type(el)):
                markdown_text += f"# {el.text}\n\n"
            elif "unstructured.documents.elements.NarrativeText" in str(type(el)):
                markdown_text += f"{el.text}\n\n"
            elif "unstructured.documents.elements.ListItem" in str(type(el)):
                # 간단한 목록 항목 처리 (실제로는 들여쓰기 수준 등을 고려해야 함)
                markdown_text += f"- {el.text}\n"
            elif "unstructured.documents.elements.Table" in str(type(el)):
                markdown_text += "## Table\n"
                markdown_text += f"{el.metadata.text_as_html}\n\n"
            else:
                markdown_text += f"{el.text}\n"
        
        # --- 단계 1: 마크다운 헤더를 기준으로 1차 분할 ---
        # [수정된 부분]
        # chunk_size 대신, 어떤 헤더를 기준으로 나눌지 정의합니다.
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]

        # MarkdownHeaderTextSplitter를 올바른 인자로 생성합니다.
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        docs_lvl1 = markdown_splitter.split_text(markdown_text)


        # --- 단계 2: 1차 분할된 청크가 너무 길 경우, 글자 수 기준으로 2차 분할 ---
        # 이 부분의 코드는 원래 의도대로 정확하게 작성되어 있었습니다.
        char_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=50,
        )
        docs = char_splitter.split_documents(docs_lvl1)

        embedding_model = HuggingFaceEmbeddings(
            model_name="dragonkue/BGE-m3-ko",
            model_kwargs={'device': self.device},
            encode_kwargs={'normalize_embeddings': True},
        )

        vectorstore = FAISS.from_documents(
            documents=docs,
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
    rag = RAG("datasets/여비산정기준표.pdf")
    print(rag.get_answer("박사과정의 월급은?"))