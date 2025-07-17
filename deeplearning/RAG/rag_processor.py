import torch
import uuid
import chromadb # chromadb 클라이언트를 직접 사용하기 위해 임포트

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
        """
        RAGProcessor 초기화 (영속성 보장 버전)
        """
        self.db_manager = db_manager
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        print(f"Using device: {self.device}")

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="dragonkue/BGE-m3-ko",
            model_kwargs={'device': self.device},
            encode_kwargs={'normalize_embeddings': True},
        )
        self.llm = OllamaLLM(model="gemma3:4b")
        
        # --- 영속성을 위한 ChromaDB 설정 ---
        # 벡터 데이터를 영구적으로 저장할 폴더 경로
        self.persist_directory = "/chroma_db_persistent_store"
        
        # 디스크에 저장된 데이터를 사용하는 ChromaDB 클라이언트 초기화
        self.chroma_client = chromadb.PersistentClient(path=self.persist_directory)
        
        # 모든 문서의 벡터를 저장할 단일 컬렉션 이름
        self.collection_name = "rag_main_collection"
        
        # LangChain과 호환되는 Chroma 벡터스토어 인스턴스 생성
        # 이 인스턴스는 클래스 내에서 계속 재사용됩니다.
        self.vectorstore = Chroma(
            client=self.chroma_client,
            collection_name=self.collection_name,
            embedding_function=self.embedding_model,
        )
        
        print(f"✅ ChromaDB가 '{self.persist_directory}' 경로에서 성공적으로 로드되었습니다.")
        print(f"현재 컬렉션 '{self.collection_name}'의 아이템 개수: {self.vectorstore._collection.count()}")


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
        """PDF를 처리하고, 벡터화하여 단일 컬렉션에 메타데이터와 함께 저장합니다."""
        print(f"'{file_path}' 파일 처리 시작 (문서 ID: {document_id})...")
        docs = self._preprocess_pdf(file_path)
        
        if not docs:
            print("⚠️ 경고: PDF에서 텍스트를 추출하지 못했거나 내용이 없습니다.")
            return False

        # 각 텍스트 조각(청크)에 메타데이터를 추가합니다.
        # "document_id"를 통해 어떤 문서에서 온 조각인지 구분할 수 있습니다.
        for doc in docs:
            doc.metadata = {"document_id": str(document_id)}

        # 미리 생성된 vectorstore 인스턴스의 단일 컬렉션에 새로운 문서 조각들을 '추가'합니다.
        self.vectorstore.add_documents(documents=docs)
        
        print(f"✅ 문서 ID {document_id}에 대한 벡터 저장 완료. 총 {len(docs)}개 조각.")
        print(f"이제 컬렉션 '{self.collection_name}'의 총 아이템 개수: {self.vectorstore._collection.count()}")
        
        # 중요: 이제 MySQL의 Document_Chunks 테이블에 메타데이터를 저장할 필요가 없습니다.
        return True


    def get_answer_from_document(self, question, document_id):
        """
        질문과 document_id를 받아, 해당 문서의 내용만을 바탕으로 답변을 생성합니다.
        """
        print(f"문서 ID {document_id}의 내용으로 질문에 답변을 생성합니다.")
        
        # --- 특정 문서의 내용만 검색하도록 Retriever 설정 ---
        # ChromaDB의 메타데이터 필터링 기능을 사용하여
        # 현재 질문과 관련된 `document_id`를 가진 조각들만 검색 대상으로 삼습니다.
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5, "filter": {"document_id": str(document_id)}}
        )

        prompt = PromptTemplate.from_template(
            """당신은 질문-답변 과제를 수행하는 어시스턴트입니다. 
            검색된 다음 컨텍스트 조각을 사용하여 질문에 답변하세요. 
            답변은 반드시 한국어로 작성해야 합니다.

            #컨텍스트: {context}
            #질문: {question}
            #답변:"""
        )

        # LangChain Expression Language (LCEL)을 사용한 체인 구성
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        # 체인 실행 및 결과 반환
        result = chain.invoke(question)
        
        # 답변의 근거가 된 컨텍스트 조각들을 함께 반환 (디버깅 및 확인용)
        retrieved_docs = retriever.invoke(question)
        context_for_log = "\n---\n".join([doc.page_content for doc in retrieved_docs])
        
        return {"answer": result, "context": context_for_log}
