# app.py
from flask import Flask, request, jsonify
import os
import uuid # 세션 ID 생성을 위해 uuid 모듈 import
import os
from tasks import build_rag_task # Celery task import

app = Flask(__name__)

# 업로드된 파일을 저장할 디렉토리 설정
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

rag_cache = {} # 세션 ID별 RAGApp 인스턴스를 저장할 딕셔너리


@app.route('/upload', methods=['POST'])
def upload_file():
    """ 📄 웹 서버로부터 PDF 파일을 받아 RAG 파이프라인을 초기화하는 API """
    global rag_app
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "파일이 존재하지 않습니다."}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"status": "error", "message": "파일이 선택되지 않았습니다."}), 400

    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            # 고유한 세션 ID 생성
            session_id = str(uuid.uuid4())
            # Celery 태스크로 RAG 빌드 작업 비동기 실행
            task = build_rag_task.delay(filepath, session_id)

            return jsonify({
                "status": "success",
                "message": f"'{file.filename}' 파일 업로드 및 RAG 빌드 작업이 시작되었습니다.",
                "session_id": session_id,
                "task_id": task.id # 클라이언트가 작업 상태를 추적할 수 있도록 task_id 반환
            }), 200
        except Exception as e:
            # RAG 파이프라인 설정 중 에러가 발생하면 클라이언트에게 알립니다.
            print(f"RAG 파이프라인 설정 중 오류 발생: {e}")
            return jsonify({"status": "error", "message": f"파일 처리 중 오류 발생: {e}"}), 500
    else:
        return jsonify({"status": "error", "message": "PDF 파일만 업로드 가능합니다."}), 400


@app.route('/ask', methods=['POST'])
def ask_question():
    """ ❓ 업로드된 PDF에 대해 질문하고 답변을 받는 API """

    if not request.is_json:
        return jsonify({"status": "error", "message": "요청 형식이 JSON이 아닙니다."}), 400
        
    data = request.get_json()
    question = data.get('question', None)
    
    if not question:
        return jsonify({"status": "error", "message": "질문(question)이 없습니다."}), 400
    
    session_id = data.get('session_id', None)
    if not session_id:
        return jsonify({"status": "error", "message": "세션 ID가 필요합니다."}), 400

    try:
        # 캐시에서 RAGApp 인스턴스 로드 또는 빌드 상태 확인
        if session_id not in rag_cache:
            # Celery 작업 상태 확인 (선택 사항, 클라이언트에서 task_id로 직접 확인 가능)
            # task = build_rag_task.AsyncResult(task_id_associated_with_session)
            # if not task.ready():
            #     return jsonify({"status": "pending", "message": "RAG 빌드 작업이 아직 완료되지 않았습니다."}), 202
            # else:
            #     # 작업 완료 후 결과 (pkl 파일 경로)를 사용하여 RAGApp 로드
            #     dump_path = task.result
            #     import pickle # 또는 dill
            #     with open(dump_path, "rb") as f:
            #         rag_cache[session_id] = pickle.load(f) # 또는 dill.load(f)
            return jsonify({"status": "error", "message": "유효하지 않은 세션 ID이거나 RAG 빌드 작업이 완료되지 않았습니다. 먼저 PDF를 업로드해주세요."}), 400

        print(f"수신된 질문: {question}")
        
        # RAG 파이프라인을 통해 답변 생성
        answer = rag_app.ask_question(question)
        
        print(f"생성된 답변: {answer}")
        return jsonify({"status": "success", "answer": answer}), 200

    except Exception as e:
        print(f"답변 생성 중 오류 발생: {e}")
        return jsonify({"status": "error", "message": f"답변 생성 중 오류 발생: {e}"}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)