import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from test_rag import RAG

# --- OpenAI API 키 설정 ---
# 코드를 실행하기 전에 터미널에서 OpenAI API 키를 환경 변수로 설정해야 합니다.
# 예: export OPENAI_API_KEY="your_openai_api_key"
# os.environ["OPENAI_API_KEY"] = "여기에 직접 키를 입력할 수도 있지만, 보안상 권장되지 않습니다."


# Flask 애플리케이션 설정
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# RAG 체인을 저장할 글로벌 변수
# 실제 프로덕션 환경에서는 사용자별 세션이나 DB를 사용하는 것이 좋습니다.
rag_chain = None

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """
    PDF 파일을 업로드하여 RAG 전처리를 수행하는 엔드포인트
    """
    global rag_chain

    if 'file' not in request.files:
        return jsonify({"error": "파일이 없습니다."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "파일이 선택되지 않았습니다."}), 400

    if file and file.filename.endswith('.pdf'):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # RAG 인스턴스를 생성하고 체인을 글로벌 변수에 저장
            rag_processor = RAG(filepath)
            rag_chain = rag_processor


            return jsonify({"message": f"'{filename}' 파일이 성공적으로 업로드 및 처리되었습니다. 이제 /ask 엔드포인트를 통해 질문할 수 있습니다."}), 200
        except Exception as e:
            return jsonify({"error": f"파일 처리 중 오류 발생: {str(e)}"}), 500
    else:
        return jsonify({"error": "PDF 파일만 업로드할 수 있습니다."}), 400


@app.route('/ask', methods=['POST'])
def ask_question():
    """
    업로드된 PDF의 내용을 바탕으로 질문에 답변하는 엔드포인트
    """
    global rag_chain

    if rag_chain is None:
        return jsonify({"error": "먼저 /upload를 통해 PDF 파일을 업로드해주세요."}), 400
    
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "질문을 JSON 형식으로 보내주세요. 예: {'question': '질문 내용'}"}), 400

    question = data['question']

    try:
        answer = rag_chain.get_answer(question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"답변 생성 중 오류 발생: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)