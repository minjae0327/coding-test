import os
import json
import requests

class pdf_to_json:
    def __init__(self):
        self.api_key = os.environ["UPSTAGE_API_KEY"]
        
        self.url = "https://api.upstage.ai/v1/document-digitization"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.data = {
            "model": "document-parse",
            "ocr": "auto",
            "chart_recognition": True,
            "coordinates": True,
            "output_formats": '["html"]',
            "base64_encoding": '["figure"]',
        }


    def convert_pdf_to_json(self, file_path):
        files = {"document": open(file_path, "rb")}
        response = requests.post(self.url, headers=self.headers, files=files, data=self.data)
        
        # Check if the request was successful
        response.raise_for_status()
        response_json = response.json()

        # Save the parsed JSON to a file
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_dir = "upstage_output"
        os.makedirs(output_dir, exist_ok=True)
        
        save_path = os.path.join(output_dir, f"{base_name}_result.json")

        with open(save_path, "w", encoding='utf-8') as f: # (수정) 인코딩 추가
            json.dump(response_json, f, indent=4, ensure_ascii=False) # (수정) 한글 깨짐 방지
        
        print(f"Upstage API 결과 저장 완료: {save_path}")
        return save_path