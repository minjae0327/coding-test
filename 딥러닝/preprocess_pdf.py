import subprocess
import os
import sys
import shutil
import unittest

class PDFPreprocessor:
    def __init__(self, original_pdf, output_ocr_pdf):
        self.original_pdf = original_pdf
        self.output_ocr_pdf = output_ocr_pdf
        
        
    def __call__(self):
        # 1) 주피터(IPython) 환경인지 확인
        try:
            # get_ipython()이 정의되어 있으면 IPython/주피터 환경으로 간주
            get_ipython  # noqa: F821
            in_jupyter = True
        except NameError:
            in_jupyter = False

        if in_jupyter:
            # 2) 주피터 환경에서는 unittest 스위트를 직접 로드하여 실행
            current_module = sys.modules[self.__class__.__module__]
            loader = unittest.defaultTestLoader
            suite = loader.loadTestsFromModule(current_module)

            # 주피터에서는 exit=False로 하지 않고, TextTestRunner로 실행해야 커널이 멈추지 않습니다
            runner = unittest.TextTestRunner(verbosity=2)
            _ = runner.run(suite)

            self.preprocess()
        else:
            # 3) 일반 스크립트/터미널 환경에서는 바로 preprocess 실행
            self.preprocess()


    def downsample_pdf(self, input_pdf_path, output_pdf_path, dpi=150):
        """
        Ghostscript를 통해 input_pdf_path를 지정한 dpi로 리샘플링하여
        output_pdf_path로 저장
        """
        # Windows에서는 gs 대신 gswin64c (또는 gswin32c)로 호출
        ghostscript_exe = "gswin64c"  # 64비트 Ghostscript
        # 만약 32비트용 Ghostscript 설치 시 "gswin32c"
        
        gs_args = [
            ghostscript_exe,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-r{dpi}",
            "-dPDFSETTINGS=/ebook",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_pdf_path}",
            input_pdf_path
        ]

        try:
            subprocess.run(gs_args, check=True)
            print(f"[정보] 리샘플링 완료: {output_pdf_path}")
        except FileNotFoundError:
            print(f"[오류] Ghostscript 실행 파일을 찾을 수 없습니다: {ghostscript_exe}")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"[오류] Ghostscript 실행 실패: {e}")
            sys.exit(1)
            

    def ocr_pdf(self, input_pdf_path, output_pdf_path, language="kor", deskew=True):
        """
        OCRmyPDF를 통해 input_pdf_path에 OCR을 수행하여 output_pdf_path로 저장
        """
        ocrmypdf_exe = "ocrmypdf"
        ocrmypdf_args = [
            ocrmypdf_exe,
            "--language", language,
            "--force-ocr",
        ]
        if deskew:
            ocrmypdf_args.append("--deskew")
        # 이미지 크기 제한 검사 해제
        ocrmypdf_args.extend(["--max-image-mpixels", "None"])
        ocrmypdf_args.extend([input_pdf_path, output_pdf_path])

        try:
            subprocess.run(ocrmypdf_args, check=True)
            print(f"[정보] OCR 완료: {output_pdf_path}")
        except FileNotFoundError:
            print(f"[오류] OCRmyPDF 실행 파일을 찾을 수 없습니다: {ocrmypdf_exe}")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"[오류] OCRmyPDF 실행 실패: {e}")
            sys.exit(1)
            

    def preprocess(self):
        # 1) 원본 PDF 경로
        # original_pdf = "datasets/manual.pdf"
        # 2) 중간(리샘플링) PDF 경로
        downsized_pdf = "datasets/downsized.pdf"
        # 3) 최종 OCR 결과 PDF 경로
        # output_ocr_pdf = "datasets/output_ocr.pdf"

        temp_dir = "temp_pdf_work"
        os.makedirs(temp_dir, exist_ok=True)

        downsized_path = os.path.join(temp_dir, os.path.basename(downsized_pdf))
        output_path = os.path.join(temp_dir, os.path.basename(self.output_ocr_pdf))

        # 1. PDF 리샘플링 (Ghostscript)
        self.downsample_pdf(self.original_pdf, downsized_path, dpi=150)

        # 2. OCR 수행 (OCRmyPDF)
        self.ocr_pdf(downsized_path, output_path, language="kor", deskew=True)

        # 결과를 지정한 위치로 복사
        shutil.copyfile(output_path, self.output_ocr_pdf)
        print(f"[완료] 최종 OCR PDF가 다음 위치에 저장되었습니다: {self.output_ocr_pdf}")

        # 임시 디렉토리 정리
        shutil.rmtree(temp_dir)