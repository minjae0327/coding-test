from my_rag import RAGRetriever, RAGGenerator

class RAGApp:
    def __init__(self, pdf_path):
        self.INPUT_PDF_PATH = pdf_path
        self.EMBEDDING_MODEL = "dragonkue/BGE-m3-ko"
        self.RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"
        self.TOKENIZER_MODEL = 'BAAI/bge-m3'
            
        self.LLM_MODEL = {
            0:"gemma3:4b",
            1:"OpenAI",
        }
        
        
    def __call__(self):
        # 1. Retriever 생성 및 설정
        retriever_handler = RAGRetriever(
            pdf_path=self.INPUT_PDF_PATH,
            embedding_model=self.EMBEDDING_MODEL,
            reranker_model=self.RERANKER_MODEL,
            tokenizer=self.TOKENIZER_MODEL
        )
        retriever_handler.setup()

        # 2. Generator 생성
        #    - 설정된 retriever를 retriever_handler로부터 가져와서 전달합니다.
        generator = RAGGenerator(
            retriever=retriever_handler.get_retriever(),
            llm_model_name=self.LLM_MODEL[0]
        )
        
        
    def ask_question(self, question):
        answer = self.generator.answer_question(question)
        
        result = "--- 최종 답변 ---\n\n" + answer
        return result