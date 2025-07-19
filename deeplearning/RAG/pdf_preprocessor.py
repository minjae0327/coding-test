import os
import json
import fitz  # PyMuPDF
import pandas as pd
import google.generativeai as genai
from PIL import Image
from bs4 import BeautifulSoup

from pdf_to_json import pdf_to_json


class pdf_preprocessor:
    def __init__(self):
        self.MAIN_PATH = "upstage_output"
        self.IMG_DIR_NAME = "md_images" # 이미지들을 모아둘 폴더 이름
        self.IMG_OUTPUT_DIR = os.path.join(self.MAIN_PATH, self.IMG_DIR_NAME)


        try:
            GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
            genai.configure(api_key=GOOGLE_API_KEY)
            
            self.text_model = genai.GenerativeModel('gemini-2.5-flash')
            self.vision_model = genai.GenerativeModel('gemini-2.5-flash')
            print("✨ Gemini models initialized successfully.")
            
        except KeyError:
            print("🛑 ERROR: GOOGLE_API_KEY environment variable not set.")
            print("Please set your API key to proceed.")
            exit()
        except Exception as e:
            print(f"🛑 ERROR: Failed to initialize Gemini models - {e}")
            exit()


    def generate_image_description_with_gemini(self, image_path):
        """
        Analyzes an image file using the Gemini API and generates a structured description.
        """
        print(f"\n--- 🖼️ Generating image description for: {os.path.basename(image_path)} ---")
        try:
            img = Image.open(image_path)
        except FileNotFoundError:
            print(f"ERROR: File not found - {image_path}")
            return "오류: 이미지 파일을 찾을 수 없어 설명을 생성하지 못했습니다."
        except Exception as e:
            print(f"ERROR: Failed to open image file - {e}")
            return "오류: 이미지 파일을 열 수 없어 설명을 생성하지 못했습니다."

        prompt = """
        당신은 이미지를 분석하여 검색 시스템(RAG)을 위한 메타데이터를 생성하는 AI 전문가입니다.
        첨부된 이미지를 RAG 시스템에서 효과적으로 검색할 수 있도록, 아래 [분석 지침]에 따라 한글로 상세히 설명해주세요.

        [분석 지침]
        1.  **종합 요약 (1~2문장)**: 이미지의 핵심 주제와 내용을 간결하게 요약해주세요.
        2.  **주요 구성요소 및 객체**: 이미지에 포함된 중요한 사물, 인물, 아이콘, 그래프 요소 등을 구체적으로 나열해주세요.
        3.  **이미지 내 텍스트 (OCR)**: 이미지에 보이는 모든 텍스트를 그대로 옮겨 적어주세요. 텍스트가 없다면 '텍스트 없음'이라고 명시해주세요.
        4.  **시각적 특징 및 스타일**: 이미지의 전체적인 색상 톤, 구도, 스타일, 분위기 등을 설명해주세요.
        5.  **핵심 키워드 (쉼표로 구분)**: 검색에 사용될 만한 핵심 키워드를 5개 이상 나열해주세요.
        """
        try:
            response = self.vision_model.generate_content([prompt, img])
            return response.text
        except Exception as e:
            print(f"ERROR during Gemini image analysis: {e}")
            return "오류: 이미지 설명을 생성하지 못했습니다."


    def generate_table_summary_with_gemini(self, table_csv_str):
        """
        Analyzes CSV string data using the Gemini API and generates a summary report.
        """
        print(f"\n--- 📊 Generating table summary ---")
        prompt = f"""
        당신은 최고의 데이터 분석가입니다. 당신의 임무는 주어진 CSV 형식의 데이터를 구조적으로 분석하고, 비전문가도 이해하기 쉽게 핵심 내용을 요약하는 것입니다.

        아래 [분석 지침]과 [CSV 데이터]를 보고 상세한 분석 보고서를 한국어로 작성해 주세요.

        [분석 지침]
        1.  **표의 주제**: 이 표가 무엇에 대한 데이터인지 한 문장으로 명확하게 정의하세요.
        2.  **구조 설명**: 각 행(row)과 열(column)이 무엇을 나타내는지 설명하세요.
        3.  **핵심 정보 및 수치**: 표에서 가장 중요한 핵심 정보를 3~5가지 항목으로 요약하세요. 구체적인 수치, 비율(%), 조건, 기간 등을 반드시 포함하세요.
        4.  **패턴 또는 특이사항 (선택 사항)**: 데이터에서 발견할 수 있는 패턴, 경향성 또는 특이점이 있다면 언급하세요.
        5.  **참고**: 데이터는 행 또는 열들의 결합으로 되어있을 수도 있습니다. 행과 열 모두 신중히 보세요.

        [CSV 데이터]
        ---
        {table_csv_str}
        ---
        """
        try:
            response = self.text_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"ERROR during Gemini table analysis: {e}")
            return "오류: 테이블 요약을 생성하지 못했습니다."


    def convert_html_to_markdown(self, element):
        html_content = element.get("content", {}).get("html", "")
        if not html_content:
            return ""

        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text().strip()

        category = element.get("category")

        # Format text based on its category
        if category == "heading1":
            # Check font size to determine heading level (#, ##, ###)
            style = soup.find().get('style', '')
            font_size = 0
            if 'font-size' in style:
                font_size = int(''.join(filter(str.isdigit, style.split('font-size:')[1])))

            if font_size >= 22:
                return f"# {text}\n"
            elif font_size >= 20:
                return f"## {text}\n"
            else:
                return f"### {text}\n"
        elif category in ["paragraph", "list"]:
            # Add extra newline for better spacing
            return f"{text}\n"
        elif category == "footer":
            return f"_{text}_\n" # Italicize footer text
        else:
            return f"{text}\n"


    def crop_element_as_image(self, pdf_doc, element, output_dir):
        page_num = element.get("page") - 1
        if page_num < 0:
            return None

        page = pdf_doc.load_page(page_num)
        page_width, page_height = page.rect.width, page.rect.height

        # Coordinates are normalized, so convert them to absolute points
        coords = element.get("coordinates", [])
        if not coords or len(coords) < 3:
            return None

        # Get the top-left (x0, y0) and bottom-right (x1, y1) points
        x0 = coords[0]['x'] * page_width
        y0 = coords[0]['y'] * page_height
        x1 = coords[2]['x'] * page_width
        y1 = coords[2]['y'] * page_height

        # Define the clipping area and get the pixmap
        clip_rect = fitz.Rect(x0, y0, x1, y1)
        # Use a high DPI for better image quality
        pix = page.get_pixmap(clip=clip_rect, dpi=200)

        # Define the image path and save it
        img_filename = f"{element.get('category')}_{element.get('id')}.png"
        img_path = os.path.join(output_dir, img_filename)
        img_path_to_store = os.path.join(self.MAIN_PATH, img_path)
        pix.save(img_path_to_store)

        print(f"✅ Saved element {element.get('id')} to {img_path_to_store}")
        return img_path


    def html_table_to_csv_string(self, html_content):
        """Converts an HTML table into a CSV formatted string."""
        try:
            # pandas.read_html returns a list of DataFrames
            df_list = pd.read_html(f"<table>{html_content}</table>", flavor='lxml')
            if not df_list:
                return ""
            # We assume the first table found is the correct one
            df = df_list[0]
            # Clean up NaN values which can occur from merged cells
            df.fillna('', inplace=True)
            return df.to_csv(index=False)
        except Exception as e:
            print(f"Could not parse HTML table: {e}")
            return ""


    def main(self, JSON_FILE_PATH, pdf_path):
        if not os.path.exists(JSON_FILE_PATH) or not os.path.exists(pdf_path):
            print(f"Error: Make sure '{JSON_FILE_PATH}' and '{pdf_path}' exist.")
            return
        
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        des_md_output_file = os.path.join(self.MAIN_PATH, f"{base_name}_with_descriptions.md")
        
        # 2. Create the output directory for images
        os.makedirs(self.IMG_OUTPUT_DIR, exist_ok=True)

        # 3. Load the JSON data
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 4. Open the PDF document
        pdf_doc = fitz.open(pdf_path)
        markdown_parts = []
        description_markdown_parts = []

        # 5. Process each element
        elements = data.get("elements", [])
        if not elements:
            print("no elements")
            return

        for element in elements:
            category = element.get("category")
            description = ""
            
            if category in ["table", "figure", "chart"]: # You can add other types here
                img_path = self.crop_element_as_image(pdf_doc, element, self.IMG_DIR_NAME)
                if img_path:
                    markdown_parts.append(f"![{category} {element.get('id')}]({img_path})\n")
                    
                if category == "table":
                    html_content = element.get("content", {}).get("html", "")
                    if html_content:
                        csv_str = self.html_table_to_csv_string(html_content)
                        if csv_str:
                            description = self.generate_table_summary_with_gemini(csv_str)
                            
                elif img_path: # Only generate description if image was successfully cropped
                    description = self.generate_image_description_with_gemini(img_path)
            
            else:
                markdown_text = self.convert_html_to_markdown(element)
                markdown_parts.append(markdown_text)
                description_markdown_parts.append(markdown_text)
                
            if description:
                formatted_description = "\n> " + description.replace("\n", "\n> ") + "\n"
                description_markdown_parts.append(formatted_description)

        with open(des_md_output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(description_markdown_parts))

        # with open(self.MD_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        #     f.write("\n".join(markdown_parts))

        print(f"\n Successfully generated Markdown file at: {des_md_output_file}")
        # print(f"\n Successfully generated Markdown file at: {self.MD_OUTPUT_FILE}")

        # 7. Clean up
        pdf_doc.close()
        
        
        return des_md_output_file

    
    def process(self, pdf_path):
        pj = pdf_to_json()
        JSON_FILE_PATH = pj.convert_pdf_to_json(pdf_path)
        
        return self.main(JSON_FILE_PATH, pdf_path)