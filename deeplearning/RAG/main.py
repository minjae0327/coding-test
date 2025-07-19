import os
import uuid
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional

# 직접 만든 모듈 임포트
from database_manager import DatabaseManager
from rag_processor2 import RAGProcessor # rag_processor2.py를 사용하도록 명시

# --- 의존성 주입을 위한 준비 ---
# 애플리케이션 생명주기 동안 단일 인스턴스를 사용
db_manager = DatabaseManager()
# (수정) RAGProcessor 초기화 시 db_manager 전달
rag_processor = RAGProcessor(db_manager)

# --- Lifespan 이벤트 핸들러 정의 ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("서버 시작: 데이터베이스 및 테이블 설정을 시작합니다.")
    db_manager.setup_tables()
    print("FastAPI 서버 시작 준비 완료.")
    
    yield # 이 지점에서 애플리케이션이 실행됩니다.
    
    # 애플리케이션 종료 시 실행될 코드 (필요 시 작성)
    print("서버 종료.")

# --- 애플리케이션 초기 설정 ---
# lifespan 핸들러를 FastAPI 앱에 등록합니다.
app = FastAPI(title="RAG Service", lifespan=lifespan)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- API 요청/응답 모델 정의 (Pydantic) ---
class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    email: str

class SessionResponse(BaseModel):
    session_id: str
    document_id: int
    session_title: str
    
class SessionInfo(BaseModel):
    session_id: str
    session_title: str

class QnALog(BaseModel):
    user_question: str
    model_answer: str

class AskRequest(BaseModel):
    question: str
    session_id: str

class AskResponse(BaseModel):
    answer: str


@app.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    """회원가입 엔드포인트"""
    hashed_password = f"hashed_{user.password}"
    try:
        # (수정) Users 테이블 스키마에 맞게 username 추가
        user_id = db_manager.execute_query(
            "INSERT INTO Users (email, password_hash) VALUES (%s, %s)",
            (user.email, hashed_password)
        )
        return UserResponse(user_id=user_id, email=user.email)
    except Exception as e:
        # (수정) MySQL 에러에서 키워드를 보고 좀 더 정확한 예외 메시지 분기
        if 'email' in str(e).lower():
            raise HTTPException(status_code=400, detail="이메일이 이미 존재합니다.")
        else:
            raise HTTPException(status_code=500, detail=f"회원가입 중 오류 발생: {str(e)}")


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """로그인 엔드포인트"""
    # (참고) FastAPI의 OAuth2PasswordRequestForm은 username 필드로 이메일을 받습니다.
    user = db_manager.execute_query(
        "SELECT * FROM Users WHERE email = %s", (form_data.username,), fetch='one'
    )
    if not user or f"hashed_{form_data.password}" != user['password_hash']:
        raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 잘못되었습니다.")
    
    return {"message": "로그인 성공", "user_id": user['user_id']}


@app.get("/sessions", response_model=List[SessionInfo])
async def get_sessions_for_user(user_id: int):
    """
    특정 사용자의 모든 세션 목록을 최신순으로 반환합니다.
    """
    sessions = db_manager.execute_query(
        "SELECT session_id, session_title FROM Sessions WHERE user_id = %s ORDER BY created_at ASC",
        (user_id,), fetch='all'
    )
    if not sessions:
        return []
    
    return sessions


@app.get("/sessions/{session_id}/history", response_model=List[QnALog])
async def get_session_history(session_id: str):
    """
    특정 세션의 모든 QnA 로그(대화 기록)를 시간순으로 반환합니다.
    """
    history = db_manager.execute_query(
        "SELECT user_question, model_answer FROM QnA_Logs WHERE session_id = %s ORDER BY timestamp ASC",
        (session_id,), fetch='all'
    )
    if not history:
        return []
    
    return history


@app.post("/sessions/create_with_pdf", response_model=SessionResponse)
async def create_session_with_pdf(user_id: int, file: UploadFile = File(...)):
    """PDF 파일을 업로드하여 새로운 채팅 세션을 생성합니다."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="PDF 파일만 업로드할 수 있습니다.")
    
    original_filename = os.path.basename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
    filepath = os.path.join(UPLOAD_DIR, unique_filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document_id = None
    try:
        doc_data = {'user_id': user_id, 'file_name': original_filename, 'file_path': filepath}
        document_id = db_manager.execute_query(
            "INSERT INTO Documents (user_id, file_name, file_path) VALUES (%s, %s, %s)",
            (doc_data['user_id'], doc_data['file_name'], doc_data['file_path'])
        )
        
        session_id = str(uuid.uuid4())
        session_title = original_filename
        db_manager.execute_query(
            "INSERT INTO Sessions (session_id, user_id, document_id, session_title) VALUES (%s, %s, %s, %s)",
            (session_id, user_id, document_id, session_title)
        )
        
        # (수정) RAG 프로세서에 document_id와 함께 session_id도 전달
        rag_processor.process_and_store_document(filepath, document_id, session_id)
        
        db_manager.execute_query("UPDATE Documents SET status = '완료' WHERE document_id = %s", (document_id,))
        
        return SessionResponse(session_id=session_id, document_id=document_id, session_title=session_title)
    except Exception as e:
        if document_id:
            db_manager.execute_query("UPDATE Documents SET status = '실패' WHERE document_id = %s", (document_id,))
        raise HTTPException(status_code=500, detail=f"세션 생성 중 오류: {str(e)}")


@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """특정 세션에 대해 질문하고 답변을 받으며, 로그를 저장합니다."""
    session = db_manager.execute_query("SELECT * FROM Sessions WHERE session_id = %s", (request.session_id,), fetch='one')
    if not session:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")

    # (수정) RAG 프로세서의 답변 생성 메서드 호출 시 document_id 전달
    # document_id가 없을 경우(문서 기반 세션이 아닐 경우)에 대한 예외 처리 추가
    doc_id = session.get('document_id')
    if not doc_id:
         raise HTTPException(status_code=404, detail="질문할 문서가 지정되지 않은 세션입니다.")

    result = rag_processor.get_answer_from_document(request.question, doc_id)
    answer = result.get('answer', "답변을 생성하지 못했습니다.")
    context = result.get('context', "")

    db_manager.execute_query(
        "INSERT INTO QnA_Logs (session_id, user_question, model_answer, retrieved_context) VALUES (%s, %s, %s, %s)",
        (request.session_id, request.question, answer, str(context))
    )
    
    return AskResponse(answer=answer)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)