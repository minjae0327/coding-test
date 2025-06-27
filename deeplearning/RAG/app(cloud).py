import os
import uuid
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify

# 직접 만든 모듈 임포트
from database_manager import DatabaseManager
from rag_processor import RAGProcessor

# --- 애플리케이션 초기 설정 ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 데이터베이스 및 RAG 처리기 인스턴스 생성
db_manager = DatabaseManager()
rag_processor = RAGProcessor(db_manager)

# 애플리케이션이 처음 시작될 때 데이터베이스 테이블 설정
with app.app_context():
    db_manager.setup_tables()
    # 테스트를 위한 사용자 생성 (실제 서비스에서는 회원가입 기능 필요)
    db_manager.execute_query(
        "INSERT IGNORE INTO Users (user_id, email, password_hash) VALUES (%s, %s, %s)",
        (1, 'test@example.com', 'hashed_password_placeholder')
    )

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """요구사항 2, 3: PDF 파일을 업로드하고, DB에 정보를 저장한 뒤, 처리하여 벡터스토어에 저장"""
    if 'file' not in request.files:
        return jsonify({"error": "파일이 없습니다."}), 400
    
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.pdf'):
        return jsonify({"error": "PDF 파일이 선택되지 않았습니다."}), 400

    # 이 예제에서는 user_id를 1로 고정합니다. 실제로는 로그인 세션에서 가져와야 합니다.
    user_id = 1
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # 2. 파일 정보를 Documents 테이블에 저장
        doc_data = {'user_id': user_id, 'file_name': filename, 'file_path': filepath}
        document_id = db_manager.execute_query(
            "INSERT INTO Documents (user_id, file_name, file_path) VALUES (%s, %s, %s)",
            (doc_data['user_id'], doc_data['file_name'], doc_data['file_path'])
        )

        if not document_id:
            return jsonify({"error": "데이터베이스에 문서 정보를 저장하는 데 실패했습니다."}), 500

        # 3. 파일을 전처리하고 벡터를 ChromaDB 및 MySQL에 저장
        rag_processor.process_and_store_document(filepath, document_id)
        
        # 문서 처리 완료 상태로 업데이트
        db_manager.execute_query("UPDATE Documents SET status = '완료' WHERE document_id = %s", (document_id,))
        
        return jsonify({
            "message": f"'{filename}' 파일이 성공적으로 처리되었습니다.",
            "document_id": document_id
        }), 200

    except Exception as e:
        # 실패 시 상태 업데이트
        if 'document_id' in locals():
            db_manager.execute_query("UPDATE Documents SET status = '실패' WHERE document_id = %s", (document_id,))
        return jsonify({"error": f"파일 처리 중 오류 발생: {str(e)}"}), 500


@app.route('/ask', methods=['POST'])
def ask_question():
    """요구사항 4: 특정 문서에 대해 질문하고, 질답 내용을 DB에 저장"""
    data = request.get_json()
    if not data or 'question' not in data or 'document_id' not in data:
        return jsonify({"error": "JSON에 'question'과 'document_id'를 포함해주세요."}), 400

    question = data['question']
    document_id = data['document_id']
    
    # 이 예제에서는 user_id를 1로 고정
    user_id = 1

    try:
        # 세션 관리를 단순화하기 위해, 요청마다 새 세션을 생성하거나 기존 세션을 찾습니다.
        # 이 예제에서는 단순화를 위해 매번 새로운 세션을 생성합니다.
        session_id = str(uuid.uuid4())
        session_title = f"문서 ID {document_id}에 대한 질문"
        db_manager.execute_query(
            "INSERT INTO Sessions (session_id, user_id, document_id, session_title) VALUES (%s, %s, %s, %s)",
            (session_id, user_id, document_id, session_title)
        )
        
        # RAG 체인을 통해 답변 생성
        result = rag_processor.get_answer_from_document(question, document_id)
        answer = result['answer']
        context = result['context'] # 검색된 컨텍스트

        # 4. 질의응답 내용을 QnA_Logs 테이블에 저장
        db_manager.execute_query(
            "INSERT INTO QnA_Logs (session_id, user_question, model_answer, retrieved_context) VALUES (%s, %s, %s, %s)",
            (session_id, question, answer, context)
        )
        
        return jsonify({"answer": answer, "session_id": session_id})

    except Exception as e:
        return jsonify({"error": f"답변 생성 중 오류 발생: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
