from flask import Flask, request, jsonify, session
from run_rag import RAGApp
import os
from datetime import timedelta

app = Flask(__name__)

# --- 세션 관리를 위한 설정 추가 ---
# 세션을 암호화하기 위한 시크릿 키입니다. 실제 서비스에서는 아무도 모르는 복잡한 값으로 바꿔야 합니다.
app.secret_key = 'your-very-secret-key-for-session' 

# 세션의 유효 기간을 설정합니다. 예를 들어 1시간 동안 유지됩니다.
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # --- 세션에 파일 경로 저장 ---
        # session은 사용자별로 유지되는 고유한 저장 공간입니다.
        session['filepath'] = filepath
        session.permanent = True # 설정한 유효 기간을 사용하도록 합니다.

        # RAG 인스턴스화 (이 부분은 기존 로직에 맞게 조정 필요)
        # rag_app_instance = RAGApp(filepath)
        # rag_app_instance()
        
        return jsonify({'message': 'File uploaded and RAG initialized successfully', 'filepath': filepath}), 200

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')

    # --- 세션에서 파일 경로 가져오기 ---
    filepath = session.get('filepath')
    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': 'RAG not initialized or file not found. Please upload a PDF first.'}), 400

    # 요청이 올 때마다 RAG 인스턴스를 생성하거나, 혹은 미리 생성된 것을 활용
    # 이 예시에서는 RAGApp의 동작 방식을 정확히 모르므로, 파일 경로만 전달하는 것으로 가정
    rag_app_instance = RAGApp(filepath)
    result = rag_app_instance.ask_question(question)

    return jsonify({'answer': result})

# --- 접속 해제 시 파일을 삭제하는 API 엔드포인트 추가 ---
@app.route('/disconnect', methods=['POST'])
def disconnect():
    """사용자가 페이지를 떠날 때 호출될 API"""
    filepath = session.get('filepath')
    
    if filepath and os.path.exists(filepath):
        try:
            os.remove(filepath)
            print(f"파일 삭제 완료: {filepath}")
            # 세션에서 파일 경로 정보도 제거
            session.pop('filepath', None)
            return jsonify({'message': 'File and session cleaned up successfully.'}), 200
        except OSError as e:
            print(f"파일 삭제 오류: {e}")
            return jsonify({'error': 'Failed to delete file.'}), 500
            
    return jsonify({'message': 'No file to clean up.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
