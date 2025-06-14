import torch
import pandas as pd
import pdfplumber

# LangChain 및 관련 라이브러리
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

# Docling 관련 라이브러리
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.chunking import HybridChunker

#OpenAI 관련 라이브러리
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# GPU 사용 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class RAGRetriever:
    """
    정보 검색(Retrieval) 단계를 담당하는 클래스.
    PDF 문서를 로드, 처리, 청킹하여 검색 가능한 Retriever를 생성합니다.
    """
    def __init__(self, pdf_path, embedding_model, reranker_model, tokenizer):
        """
        RAGRetriever 클래스를 초기화합니다.

        Args:
            pdf_path (str): 처리할 PDF 파일 경로.
            embedding_model (str): 임베딩에 사용할 HuggingFace 모델 이름.
            reranker_model (str): Reranking에 사용할 CrossEncoder 모델 이름.
        """
        self.pdf_path = pdf_path
        self.embedding_model_name = embedding_model
        self.reranker_model_name = reranker_model
        self.tokenizer = tokenizer
        self.embedding_model = None
        self.retriever = None

    def _load_and_process_pdf(self):
        """Docling을 사용하여 PDF를 처리하고 텍스트/테이블을 추출합니다."""
        print("1. Docling으로 PDF 문서 처리를 시작합니다...")
        pipeline_options = PdfPipelineOptions(
            do_table_structure=True,
            do_text_extraction=True,
        )
        pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        return doc_converter.convert(self.pdf_path)

    def _extract_tables_with_pdfplumber(self):
        """pdfplumber를 사용하여 PDF에서 테이블을 추출하고 마크다운 형식으로 변환합니다."""
        print("2. pdfplumber로 테이블을 추출합니다...")
        chunks = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    try:
                        df = pd.DataFrame(table[1:], columns=table[0])
                    except:
                        df = pd.DataFrame(table)
                    md_table = df.to_markdown(index=False)
                    chunks.append({
                        "text": md_table,
                        "metadata": {"type": "table", "page": page.page_number}
                    })
        return [Document(page_content=chunk["text"], metadata={**chunk["metadata"], "source": self.pdf_path}) for chunk in chunks]

    def _create_documents_from_chunks(self, docling_doc):
        """Docling 처리 결과와 pdfplumber 테이블 결과를 LangChain Document 리스트로 변환합니다."""
        print("3. 텍스트와 테이블을 LangChain 문서 형식으로 변환합니다...")
        # Docling을 사용한 텍스트 청킹
        chunker = HybridChunker(
            tokenizer=self.tokenizer,
            max_token_length=512,
            overlap=100
        )
        text_chunks = list(chunker.chunk(docling_doc.document))

        text_documents = []
        for chunk in text_chunks:
            page_nos = sorted(set(prov.page_no for item in chunk.meta.doc_items for prov in item.prov if hasattr(prov, "page_no")))
            headings = chunk.meta.headings if hasattr(chunk.meta, "headings") else []
            metadata = {
                "source": self.pdf_path,
                "page_numbers": page_nos,
                "section": headings[-1] if headings else None
            }
            text_documents.append(Document(page_content=chunk.text, metadata=metadata))

        # pdfplumber로 추출한 테이블 문서
        table_documents = self._extract_tables_with_pdfplumber()

        return table_documents + text_documents

    def setup(self):
        """
        모든 설정 단계를 실행하여 최종 Retriever를 생성합니다.
        """
        # 1. 문서 로드 및 처리
        docling_doc = self._load_and_process_pdf()

        # 2. 문서 형식 변환 및 통합
        all_documents = self._create_documents_from_chunks(docling_doc)
        print(f"총 {len(all_documents)}개의 문서(청크)를 생성했습니다.")

        # 3. 임베딩 모델 로드
        print(f"4. 임베딩 모델({self.embedding_model_name})을 로드합니다...")
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={'device': device},
            encode_kwargs={'normalize_embeddings': True},
        )

        # 4. 벡터 저장소 구축
        print("5. FAISS 벡터 저장소를 구축합니다...")
        vectorstore = FAISS.from_documents(
            documents=all_documents,
            embedding=self.embedding_model
        )
        base_retriever = vectorstore.as_retriever()

        # 5. Reranker 설정 및 최종 Retriever 생성
        print(f"6. Reranker({self.reranker_model_name})를 설정합니다...")
        cross_encoder_model = HuggingFaceCrossEncoder(model_name=self.reranker_model_name)
        compressor = CrossEncoderReranker(model=cross_encoder_model, top_n=3)
        self.retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=base_retriever
        )
        print("Retriever 설정이 완료되었습니다.")

    def get_retriever(self):
        """생성된 retriever 객체를 반환합니다."""
        if not self.retriever:
            raise RuntimeError("Retriever가 설정되지 않았습니다. 먼저 setup() 메서드를 호출하세요.")
        return self.retriever


class RAGGenerator:
    """
    답변 생성(Generation) 단계를 담당하는 클래스.
    Retriever로부터 받은 정보를 바탕으로 LLM을 사용하여 답변을 생성합니다.
    """
    def __init__(self, retriever, llm_model_name):
        """
        RAGGenerator 클래스를 초기화합니다.

        Args:
            retriever: RAGRetriever 클래스에서 생성된 retriever 객체.
            llm_model_name (str): 사용할 Ollama 모델 이름.
        """
        self.retriever = retriever
        self.llm_model_name = llm_model_name
        if llm_model_name == "OpenAI":
            self.llm = ChatOpenAI(model_name = "gpt-4o-mini", temperature=0)            
        else:
            self.llm = OllamaLLM(model=self.llm_model_name)
        self.chain = self._build_chain()

    @staticmethod
    def _format_docs(docs):
        """검색된 문서들을 LLM 프롬프트에 넣기 좋은 형태로 포맷합니다."""
        return '\n\n'.join(doc.page_content for doc in docs)

    def _build_chain(self):
        """RAG 체인을 구성합니다."""
        prompt = ChatPromptTemplate.from_template("""
            You are an assistant for question-answering tasks. 
            Use the following pieces of retrieved context to answer the question.
            If the user asks for a simple answer, summarize the key points.
            If the question is unrelated to the context in the regulations, respond with "관련 정보를 찾을 수 없습니다."
            You must answer in Korean.

            #Context: 
            {context}

            #Question:
            {question}

            #Answer:
            """)
        
        rag_chain = (
            {'context': self.retriever | self._format_docs, 'question': RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        return rag_chain

    def answer_question(self, question):
        """
        질문에 대한 답변을 생성합니다.

        Args:
            question (str): 사용자 질문.

        Returns:
            str: LLM이 생성한 답변.
        """
        print("\n질문을 처리 중입니다...")
        return self.chain.invoke(question)
