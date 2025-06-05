from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 파일 경로 설정
input_pdf = "datasets/여비산정기준표.pdf"
preprocessed_file = "datasets/ocr_output.pdf"
result_file = "datasets/ocr_output_result.pdf",



from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode

pipeline_options = PdfPipelineOptions(
    do_table_structure = True,
    do_text_extraction=True,
)
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

doc = doc_converter.convert(input_pdf)

markdown_text = doc.document.export_to_markdown()
# print(markdown_text)
#읽지 못하는 텍스트와 사진 처리방법 고민



import pdfplumber
import pandas as pd

def table_chunker(pdf_path: str):
    chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                # table: 2D 리스트 (헤더 포함)
                try:
                    df = pd.DataFrame(table[1:], columns=table[0])
                except:
                    df = pd.DataFrame(table)
                md_table = df.to_markdown(index=False)
                chunks.append({
                    "text": md_table,
                    "metadata": {
                        "type": "table",
                        "page": page.page_number
                    }
                })
    return chunks



# 사용 예시
table_chunks = table_chunker(input_pdf)

from docling.chunking import HybridChunker

chunker = HybridChunker(
    tokenizer='BAAI/bge-m3',
    max_token_length=512,
    overlap=100
)

chunks = list(chunker.chunk(doc.document))

# chunks는 청커로 생성된 문서 조각들
# documents = [Document(page_content=chunk.text, metadata={"source": chunk.meta}) for chunk in chunks]



text_documents = []
for chunk in chunks:
    text = chunk.text

    source = input_pdf

    # page_no를 추출 (여러 Prov 아이템 중 첫 번째의 page_no를 사용하거나, set으로 처리)
    page_nos = sorted(
        set(
            prov.page_no
            for item in chunk.meta.doc_items
            for prov in item.prov
            if hasattr(prov, "page_no")
        )
    ) if hasattr(chunk.meta, "doc_items") else []

    # 가장 근접한 헤딩(섹션 이름) 추출 (예: 마지막 요소)
    headings = chunk.meta.headings if hasattr(chunk.meta, "headings") else []
    section = headings[-1] if headings else None

    metadata = {
        "source": source,
        "page_numbers": page_nos,
        "section": section
    }
    # (3) LangChain Document 생성
    text_documents.append(Document(page_content=text, metadata=metadata))
    
    
    # 1. table_chunks를 Document 형식으로 변환
table_documents = [
    Document(
        page_content=chunk["text"],
        metadata={
            "type": "table",
            "page": chunk["metadata"]["page"],
            "source": input_pdf
        }
    ) for chunk in table_chunks
]

# 3. 두 Document 리스트 합치기
all_documents = table_documents + text_documents



embedding_model = HuggingFaceEmbeddings(
    model_name="dragonkue/BGE-m3-ko",
    model_kwargs={'device': device},
    encode_kwargs={'normalize_embeddings': True},
)

vectorstore = FAISS.from_documents(
    documents=all_documents,
    embedding=embedding_model
)

retriever = vectorstore.as_retriever()




from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

# 모델 초기화
model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")

# 상위 3개의 문서 선택
compressor = CrossEncoderReranker(model=model, top_n=3)

# 문서 압축 검색기 초기화
compression_reranker = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)



from langchain_ollama import OllamaLLM

# llm = OllamaLLM(model="llama3.2:3b")
# llm = OllamaLLM(model="deepseek-r1:1.5b")
llm = OllamaLLM(model="gemma3:4b")
# llm = ChatOpenAI(model_name = "gpt-4o-mini", temperature=0)

def format_docs(docs):
    return '\n\n'.join(doc.page_content for doc in docs)

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
    {'context': compression_reranker | format_docs, 'question': RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


question = "교수가 미국으로 4일 출장을 다녀오면 받을 수 있는 숙박비는?"
result = rag_chain.invoke(question)
print(result)