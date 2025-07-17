"""
rag_processor.py에서 pdf를 전처리하는 클래스
제작 중
"""

import os
import time
from openai import OpenAI

# API 클라이언트 초기화
client = OpenAI()

def analyze_csv_with_assistant(file_path):
    """
    Assistant API와 Code Interpreter를 사용하여 CSV 파일을 분석하고 요약합니다.
    """
    # 1. 파일 업로드
    print(f"1. '{file_path}' 파일 업로드 중...")
    try:
        file_object = client.files.create(
            file=open(file_path, "rb"),
            purpose="assistants"
        )
    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다 - {file_path}")
        return None
        
    print(f"   - 파일 ID: {file_object.id}")

    # 2. 어시스턴트 생성 (Code Interpreter 활성화)
    print("2. 데이터 분석용 어시스턴트 생성 중...")
    assistant = client.beta.assistants.create(
        name="데이터 분석가",
        instructions="당신은 데이터 분석 전문가입니다. 주어진 CSV 파일을 분석하고, 그 구조와 핵심 내용을 설명해야 합니다.",
        model="gpt-4o-mini",
        tools=[{"type": "code_interpreter"}]
    )
    print(f"   - 어시스턴트 ID: {assistant.id}")

    # 3. 대화를 위한 스레드 생성
    print("3. 대화 스레드 생성 중...")
    thread = client.beta.threads.create()
    print(f"   - 스레드 ID: {thread.id}")

    # 4. 스레드에 메시지 및 파일 추가
    print("4. 분석 요청 메시지 및 파일 추가 중...")
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"첨부된 CSV 파일을 분석해서 다음 항목에 따라 보고서를 작성해 주세요:\n1. 표의 주제\n2. 구조(행, 열) 설명\n3. 핵심 정보 및 수치 요약\n4. 데이터 패턴 또는 특이사항\n\n이 보고서는 한국어로 작성되어야 합니다.",
        attachments=[{"file_id": file_object.id, "tools": [{"type": "code_interpreter"}]}]
    )

    # 5. 어시스턴트 실행
    print("5. 어시스턴트 실행 및 분석 시작...")
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # 6. 실행 완료 대기
    while run.status not in ["completed", "failed"]:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"   - 현재 상태: {run.status}")
        time.sleep(3)

    if run.status == "completed":
        print("6. 분석 완료. 결과 가져오는 중...")
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        # 가장 최근의 어시스턴트 응답을 찾습니다.
        for message in messages.data:
            if message.role == "assistant":
                summary = message.content[0].text.value
                # 리소스 정리 (선택 사항)
                client.beta.assistants.delete(assistant.id)
                client.files.delete(file_object.id)
                client.beta.threads.delete(thread.id)
                return summary
    else:
        print(f"오류: 분석 실패 - {run.last_error}")
        return None


# --- 사용 예시 ---
# process_table_with_ai_camelot 함수 내에서 아래 코드를 호출할 수 있습니다.
table_path = "manual/tables/p1_tbl0.csv" # 예시 파일 경로
summary = analyze_csv_with_assistant(table_path)
if summary:
    print("\n--- 최종 분석 결과 ---")
    print(summary)