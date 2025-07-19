import os
import re
import uuid
import torch
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

# from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from pdf_preprocessor import pdf_preprocessor


class RAGProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        self.vectorstore = None
        self.persist_directory = "./chroma_db"
        
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="dragonkue/BGE-m3-ko",
            model_kwargs={'device': self.device},
            encode_kwargs={'normalize_embeddings': True},
        )
        
        # (수정) 서버 시작 시 디스크에 저장된 벡터 DB를 불러오는 로직
        if os.path.exists(self.persist_directory):
            print(f"기존 벡터 DB를 로드합니다: {self.persist_directory}")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_model
            )
        else:
            print("기존 벡터 DB가 없어 새로 생성됩니다.")
            self.vectorstore = None
        
        
    def create_documents_from_markdown(self, markdown_content, source_path, document_id):
        # 기존의 논리적 청킹 함수를 그대로 사용합니다.
        text_chunks = self.chunk_markdown_logically(markdown_content)
        
        documents = []
        for chunk_text in text_chunks:
            metadata = {"source": source_path, "document_id": str(document_id)}  # 모든 청크에 기본 출처 정보 추가
            
            # 청크 내용을 기반으로 추가 메타데이터 파싱
            if chunk_text.startswith("[[-- TABLE:"):
                metadata['type'] = 'table'
                # 정규표현식을 사용하여 페이지 번호와 경로 추출
                page_match = re.search(r"Page (\d+)", chunk_text)
                path_match = re.search(r"Path: (.*?)\s*--]]", chunk_text)
                if page_match:
                    metadata['page'] = int(page_match.group(1))
                if path_match:
                    metadata['table_path'] = path_match.group(1).strip()

            elif chunk_text.startswith("!["):
                metadata['type'] = 'image'
                # 정규표현식을 사용하여 페이지 번호와 이미지 설명 추출
                page_match = re.search(r"Image from page (\d+)", chunk_text)
                desc_match = re.search(r"!\[(.*?)\]\(", chunk_text)
                if page_match:
                    metadata['page'] = int(page_match.group(1))
                if desc_match:
                    metadata['description'] = desc_match.group(1).strip()
            else:
                metadata['type'] = 'text'

            # Document 객체 생성
            doc = Document(page_content=chunk_text, metadata=metadata)
            documents.append(doc)
            
        return documents

    # --- 2. 기존 로직 실행 및 all_chunks 생성 ---

    # chunk_markdown_logically 함수는 제공된 코드에 이미 정의되어 있다고 가정합니다.
    def chunk_markdown_logically(self, markdown_content):
        """
        문서의 구조(제목, 표, 이미지)를 이해하여 논리적인 단위로 청킹합니다.
        RAG 시스템에 가장 효과적인 방법입니다.
        """
        # 1. 기본 블록으로 분리
        blocks = markdown_content.split('\n\n')
        
        chunks = []
        current_chunk = ""

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            # 2. 규칙에 따라 청크 생성
            is_table_placeholder = block.startswith("[[-- TABLE:")
            is_image_link = block.startswith("![")
            # 제목으로 사용될 수 있는 패턴들 (필요에 따라 추가)
            is_heading = block.startswith(('□', '○', '※')) or re.match(r'^[0-9]+\s|^\w+\s', block) and len(block) < 50

            if is_table_placeholder or is_image_link:
                # 테이블/이미지는 독립적인 청크로 처리
                if current_chunk:
                    chunks.append(current_chunk.strip())
                chunks.append(block)
                current_chunk = ""
            elif is_heading:
                # 제목은 다음 블록과 합치기 위해, 진행 중인 청크를 먼저 저장
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = block
            else:
                # 일반 텍스트는 현재 청크(제목 또는 이전 텍스트)에 추가
                if current_chunk:
                    current_chunk += "\n\n" + block
                else:
                    current_chunk = block
        
        # 마지막 남은 청크 추가
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
     
    
    def store_documents(self, all_chunks, session_id):
        """ChromaDB에 문서를 저장하고, 메타데이터를 SQL DB에 기록합니다."""
        if not all_chunks:
            print("저장할 문서 조각이 없습니다.")
            return

        # (수정) 각 청크에 대한 고유 ID 생성 (SQL DB와 벡터 DB 연결고리)
        chunk_ids = [str(uuid.uuid4()) for _ in all_chunks]
        
        # (수정) 기존 DB에 데이터를 추가하는 방식으로 변경, IDs 지정
        if self.vectorstore is None:
            # 첫 업로드 시, 새로운 벡터 저장소 생성
            self.vectorstore = Chroma.from_documents(
                documents=all_chunks,
                embedding=self.embedding_model,
                ids=chunk_ids,
                persist_directory=self.persist_directory
            )
        else:
            # 기존 벡터 저장소에 문서 추가
            self.vectorstore.add_documents(documents=all_chunks, ids=chunk_ids)

        # (수정) db_manager를 사용하여 Document_Chunks 테이블에 정보 저장
        print(f"'{session_id}' 세션에 대한 문서 조각 {len(all_chunks)}개를 DB에 저장합니다.")
        for doc, vector_id in zip(all_chunks, chunk_ids):
            self.db_manager.execute_query(
                "INSERT INTO Document_Chunks (session_id, chunk_text, vector_id) VALUES (%s, %s, %s)",
                (session_id, doc.page_content, vector_id)
            )
    
    
    def process_and_store_document(self, filepath, document_id, session_id):
        pp = pdf_preprocessor()
        with open(pp.process(filepath), 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        all_chunks = self.create_documents_from_markdown(md_content, filepath, document_id)
        self.store_documents(all_chunks, session_id)
        
        
    def get_answer_from_document(self, question, document_id):
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5, "filter": {"document_id": str(document_id)}}
        )


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


        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        chain = (
            {"context": retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        answer = chain.invoke(question)
        return answer