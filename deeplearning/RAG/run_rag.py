# from my_rag import RAGRetriever, RAGGenerator

# class RAGApp:
#     def __init__(self, pdf_path):
#         self.INPUT_PDF_PATH = pdf_path
#         self.EMBEDDING_MODEL = "dragonkue/BGE-m3-ko"
#         self.RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"
#         self.TOKENIZER_MODEL = 'BAAI/bge-m3'
            
#         self.LLM_MODEL = {
#             0:"gemma3:4b",
#             1:"OpenAI",
#         }
        
        
#     def __call__(self):
#         # 1. Retriever 생성 및 설정
#         retriever_handler = RAGRetriever(
#             pdf_path=self.INPUT_PDF_PATH,
#             embedding_model=self.EMBEDDING_MODEL,
#             reranker_model=self.RERANKER_MODEL,
#             tokenizer=self.TOKENIZER_MODEL
#         )
#         retriever_handler.setup()

#         # 2. Generator 생성
#         #    - 설정된 retriever를 retriever_handler로부터 가져와서 전달합니다.
#         self.generator = RAGGenerator(
#             retriever=retriever_handler.get_retriever(),
#             llm_model_name=self.LLM_MODEL[0]
#         )
        
        
#     def ask_question(self, question):
#         answer = self.generator.answer_question(question)
        
#         result = "--- 최종 답변 ---\n\n" + answer
#         return result

# run_rag.py (수정된 최종 버전)


from my_rag import RAGRetriever, RAGGenerator
from transformers import AutoTokenizer #! 1. AutoTokenizer를 import 합니다.

class RAGApp:
    def __init__(self, pdf_path):
        """
        RAGApp 객체 생성 시 모든 초기화(모델 로딩, 리트리버/제너레이터 설정)를 완료합니다.
        __call__ 메소드를 제거하고 모든 로직을 __init__으로 이동했습니다.
        """
        # self.INPUT_PDF_PATH = pdf_path
        # self.EMBEDDING_MODEL = "jhgan/ko-sbert-nli" # 한국어 모델로 변경 권장
        # self.RERANKER_MODEL = "kiyoung2/ko-kce-dev-v1" # 한국어 모델로 변경 권장
        # self.TOKENIZER_MODEL_NAME = "jhgan/ko-sbert-nli" # 임베딩 모델과 맞춰주는 것이 일반적
        self.INPUT_PDF_PATH = pdf_path
        self.EMBEDDING_MODEL = "dragonkue/BGE-m3-ko"
        self.RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"
        self.TOKENIZER_MODEL = 'BAAI/bge-m3'
            
        self.LLM_MODEL = {
            0: "gemma3:4b", # Ollama 모델
            1: "OpenAI",   # OpenAI 모델
        }
        
        
    def set_rag_model(self):
        #! 2. 토크나이저 모델 이름(문자열)으로 실제 토크나이저 객체를 로드합니다.
        tokenizer_object = AutoTokenizer.from_pretrained(self.TOKENIZER_MODEL)

        # 1. Retriever 생성 및 설정
        #    - tokenizer 인자로 문자열 대신 생성된 토크나이저 객체를 전달합니다.
        retriever_handler = RAGRetriever(
            pdf_path=self.INPUT_PDF_PATH,
            embedding_model=self.EMBEDDING_MODEL,
            reranker_model=self.RERANKER_MODEL,
            tokenizer=tokenizer_object #! 3. 생성된 객체를 전달
        )
        retriever_handler.setup() # PDF 처리 및 리트리버 구축 실행

        # 2. Generator 생성
        #    - 설정된 retriever를 retriever_handler로부터 가져와서 전달합니다.
        self.generator = RAGGenerator(
            retriever=retriever_handler.get_retriever(),
            llm_model_name=self.LLM_MODEL[0] # gemma:2b 모델 사용
        )
        
        
        
    def ask_question(self, question):
        if not self.generator:
            raise RuntimeError("Generator가 초기화되지 않았습니다.")
            
        answer = self.generator.answer_question(question)
        
        result = "--- 최종 답변 ---\n\n" + answer
        return result