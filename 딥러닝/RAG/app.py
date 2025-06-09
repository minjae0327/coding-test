# 1. '우체국' 역할을 할 Flask 라이브러리 임포트
from flask import Flask, request, jsonify

# 2. '업무 담당자'의 실제 업무 로직 (지난 답변에서 작성한 RAG 검색 함수)
from 딥러닝.RAG.my_rag import search_company_documents

# Flask 앱(우체국) 생성
app = Flask(__name__)

# 3. 특정 주소('/mcp')로 오는 POST 요청(편지)을 처리할 창구 마련
@app.route('/mcp', methods=['POST'])
def handle_mcp_request():
    # Flask가 HTTP 요청 본문을 JSON으로 파싱 (편지 개봉)
    mcp_request = request.json

    # MCP 프로토콜(편지 양식)에 따라 내용 분석 및 처리
    # 이 부분이 바로 'MCP 서버 로직'입니다.
    method = mcp_request.get("method")
    params = mcp_request.get("params")
    
    response_data = None
    if method == "resources/get" and params["uri"].startswith("company-docs://search"):
        try:
            query = params["uri"].split("?query=")[1]
            # 실제 RAG 검색 로직 호출
            documents = search_company_documents(query)
            response_data = {
                "jsonrpc": "2.0",
                "result": {
                    "content": "\n\n---\n\n".join(documents),
                    "media_type": "text/plain"
                },
                "id": mcp_request.get("id")
            }
        except Exception as e:
            # 에러 처리 로직
            pass
    else:
        # 지원하지 않는 메소드에 대한 에러 처리
        pass

    # Flask를 통해 처리 결과를 JSON 형태로 응답 (답장 발송)
    return jsonify(response_data)

# '우체국' 운영 시작
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)