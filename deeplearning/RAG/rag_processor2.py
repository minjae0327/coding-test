import os
import re
import uuid
import shutil
import torch
from langchain_chroma import Chroma
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
        
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="dragonkue/BGE-m3-ko",
            model_kwargs={'device': self.device},
            encode_kwargs={'normalize_embeddings': True},
        )
        
        
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
     
    
    
    def process_and_store_document(self, filepath, user_id, session_id, session_path):
        """
            pp.process()를 사용해서 pdf파일을 .md 파일로 변환
            지정된 경로에 vectorstore 저장
            그 후 vectorstore를 제외한 모든 파일 삭제
        """
        
        pp = pdf_preprocessor(session_path)
        
        md_file_path = pp.process(filepath)
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        all_chunks = self.create_documents_from_markdown(md_content, filepath, session_id)
    
        vector_store_path = os.path.join(session_path, "vector_store")
        os.makedirs(vector_store_path, exist_ok=True)
        
        print(f"새로운 벡터스토어를 {vector_store_path}에 저장합니다")
        vectorstore = Chroma.from_documents(
            documents=all_chunks,
            embedding=self.embedding_model,
            persist_directory=vector_store_path
        )
        
        return vector_store_path
        
        # print("임시 저장 파일 삭제중")
        
        # if os.path.exists(filepath):
        #     os.remove(filepath)
        #     print(f"  - 원본 PDF 삭제: {filepath}")

        # md_path_to_remove = getattr(pp, 'des_md_output_file', None)
        # if md_path_to_remove and os.path.exists(md_path_to_remove):
        #     os.remove(md_path_to_remove)
        #     print(f"  - 마크다운 파일 삭제: {md_path_to_remove}")

        # img_dir_to_remove = getattr(pp, 'IMG_DIR_NAME', None)
        # if img_dir_to_remove and os.path.exists(img_dir_to_remove):
        #     shutil.rmtree(img_dir_to_remove)
        #     print(f"  - 이미지 폴더 삭제: {img_dir_to_remove}")

        # json_dir_to_remove = os.path.join(session_path, "upstage_output")
        # if os.path.exists(json_dir_to_remove):
        #     shutil.rmtree(json_dir_to_remove)
        #     print(f"  - JSON 폴더 삭제: {json_dir_to_remove}")

        
        
    def get_answer_from_document(self, question, document_id, vector_store_path):
        """
            유저로부터 질문을 받아서 질문에 대한 답변과 가장 관련이 높은 context 하나를 return 하는 함수
        """
        if not os.path.exists(vector_store_path):
            return {"answer": "오류: 해당 세션의 벡터 데이터를 찾을 수 없습니다.", "context": ""}

        # 1. 요청에 맞는 벡터 스토어를 동적으로 로드
        vectorstore = Chroma(
            persist_directory=vector_store_path,
            embedding_function=self.embedding_model
        )
        
        
        retriever = vectorstore.as_retriever(
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
        
        all_context_docs = retriever.invoke(question)
        answer = chain.invoke(question)
        
        single_context_docs = all_context_docs[0] if all_context_docs else None
        
        return {"answer": answer, "context": single_context_docs}