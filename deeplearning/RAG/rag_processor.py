import torch
import uuid

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.text_splitter import MarkdownHeaderTextSplitter
from unstructured.partition.pdf import partition_pdf
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate


class RAGProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="dragonkue/BGE-m3-ko",
            model_kwargs={'device': self.device},
            encode_kwargs={'normalize_embeddings': True},
        )
        self.llm = OllamaLLM(model="gemma3:4b") # 또는 다른 LLM
        # ChromaDB가 저장될 디렉토리
        self.persist_directory = "chroma_db_store"


    def _preprocess_pdf(self, file_path):
        """PDF 파일을 로드하고 전처리하여 텍스트 조각(Document 객체)으로 분할합니다."""
        elements = partition_pdf(filename=file_path, strategy="hi_res")
        markdown_text = ""
        for el in elements:
            markdown_text += f"{el.text}\n\n"

        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2")]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        docs_lvl1 = markdown_splitter.split_text(markdown_text)

        char_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
        docs = char_splitter.split_documents(docs_lvl1)
        return docs


    def process_and_store_document(self, file_path, document_id):
        """PDF를 처리하고, 벡터화하여 ChromaDB에 저장한 뒤, 메타데이터를 MySQL에 저장합니다."""
        print(f"'{file_path}' 파일 처리 시작...")
        docs = self._preprocess_pdf(file_path)
        
        # 각 조각에 고유한 벡터 ID를 부여합니다.
        vector_ids = [str(uuid.uuid4()) for _ in docs]

        # Chroma 벡터 저장소 생성 및 데이터 추가
        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=self.embedding_model,
            ids=vector_ids, # 각 조각에 고유 ID 부여
            collection_name=f"doc_{document_id}", # 각 문서별로 별도의 컬렉션 사용
            persist_directory=self.persist_directory
        )
        vectorstore.persist() # 변경사항 디스크에 저장
        print(f"문서 ID {document_id}에 대한 벡터 저장 완료. 총 {len(docs)}개 조각.")

        # MySQL의 Document_Chunks 테이블에 메타데이터 저장
        for v_id in vector_ids:
            chunk_data = {
                'document_id': document_id,
                'vector_id': v_id
            }
            self.db_manager.execute_query(
                "INSERT INTO Document_Chunks (document_id, vector_id) VALUES (%s, %s)",
                (chunk_data['document_id'], chunk_data['vector_id'])
            )
        print("MySQL에 벡터 메타데이터 저장 완료.")
        return True


    def get_answer_from_document(self, question, document_id):
        """저장된 벡터 저장소를 로드하고, 질문에 대한 답변을 생성합니다."""
        # 디스크에 저장된 ChromaDB 로드
        vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model,
            collection_name=f"doc_{document_id}"
        )
        retriever = vectorstore.as_retriever()

        prompt = PromptTemplate.from_template(
            """You are an assistant for question-answering tasks. 
            Use the following pieces of retrieved context to answer the question. 
            Answer in Korean.

            #Context: {context}
            #Question: {question}
            #Answer:"""
        )

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        result = chain.invoke(question)
        # RAG 과정에서 검색된 context도 함께 반환하면 좋습니다.
        # 이 예제에서는 답변만 반환합니다.
        return {"answer": result, "context": "retrieved context here"} # context 부분은 실제 구현에서 채워야 함
