import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QTextEdit, QFrame, QStackedWidget, QListWidget, QListWidgetItem, QFileDialog
)
from PyQt6.QtCore import Qt, QSize
import os

# --- 위젯 클래스 정의 (LoginWidget, MainAppWidget) ---

class LoginWidget(QWidget):
    """로그인 및 회원가입 UI를 담당하는 위젯"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("PDF RAG")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("이메일")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("비밀번호")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("로그인")
        self.signup_button = QPushButton("회원가입")
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: red;")

        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("이메일:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("비밀번호:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.signup_button)
        layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.login_button.clicked.connect(self.login)
        self.signup_button.clicked.connect(self.signup)
        
        self.setLayout(layout)
        # 테스트를 위한 기본값 설정
        self.email_input.setText("minjae0327@gmail.com")
        self.password_input.setText("lovepool")


    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        self.parent_app.login(email, password)
    
    def signup(self):
        email = self.email_input.text()
        password = self.password_input.text()
        self.parent_app.signup(email, password)

class MainAppWidget(QWidget):
    """로그인 후의 메인 애플리케이션 UI를 담당하는 위젯"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        
        # 전체 레이아웃을 QVBoxLayout으로 변경
        top_level_layout = QVBoxLayout(self)
        top_level_layout.setContentsMargins(0, 5, 0, 0) # 상단 여백 추가

        # --- 상단 바 (로그아웃 버튼) ---
        top_bar_layout = QHBoxLayout()
        self.logout_button = QPushButton("로그아웃")
        self.logout_button.setFixedWidth(100) # 버튼 너비 고정
        top_bar_layout.addWidget(self.logout_button)
        top_bar_layout.addStretch() # 버튼을 왼쪽으로 밀기

        # --- 메인 컨텐츠 (세션 목록 + 채팅창) ---
        main_content_layout = QHBoxLayout()

        # 왼쪽: 세션 목록
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("채팅 세션 목록"))
        self.session_list = QListWidget()
        self.new_chat_button = QPushButton("새로운 PDF로 채팅 시작")
        left_panel.addWidget(self.session_list)
        left_panel.addWidget(self.new_chat_button)
        
        # 오른쪽: 채팅 화면
        right_panel = QVBoxLayout()
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("질문을 입력하세요...")
        self.send_button = QPushButton("전송")
        
        question_layout = QHBoxLayout()
        question_layout.addWidget(self.question_input)
        question_layout.addWidget(self.send_button)
        
        right_panel.addWidget(self.chat_display)
        right_panel.addLayout(question_layout)

        main_content_layout.addLayout(left_panel, 1)
        main_content_layout.addLayout(right_panel, 3)
        
        # 전체 레이아웃에 상단 바와 메인 컨텐츠 추가
        top_level_layout.addLayout(top_bar_layout)
        top_level_layout.addLayout(main_content_layout)

        # --- 시그널 연결 ---
        self.logout_button.clicked.connect(self.parent_app.logout)
        self.new_chat_button.clicked.connect(self.parent_app.start_new_session)
        self.send_button.clicked.connect(self.parent_app.ask_question)
        self.session_list.currentItemChanged.connect(self.parent_app.session_selected)
        self.question_input.returnPressed.connect(self.parent_app.ask_question)


# --- 메인 애플리케이션 클래스 ---

class RAGClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.server_url = "http://175.125.143.96:5000"
        self.server_url = "http://127.0.0.1:5000"
        self.user_id = None
        self.current_session_id = None
        
        self.setWindowTitle("PDF 기반 RAG 시스템")
        self.setGeometry(200, 200, 1000, 700)
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.login_widget = LoginWidget(self)
        self.main_app_widget = MainAppWidget(self)
        
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.main_app_widget)

    def login(self, email, password):
        try:
            response = requests.post(
                f"{self.server_url}/login",
                data={"username": email, "password": password}
            )
            if response.status_code == 200:
                self.user_id = response.json()['user_id']
                self.stacked_widget.setCurrentWidget(self.main_app_widget)
                self.load_sessions() # **수정: 로그인 후 세션 목록 로드**
            else:
                self.login_widget.status_label.setText(response.json().get('detail', '로그인 실패'))
        except requests.RequestException as e:
            self.login_widget.status_label.setText(f"서버 연결 오류: {e}")

    def logout(self):
        """로그아웃 처리"""
        self.user_id = None
        self.current_session_id = None
        self.main_app_widget.session_list.clear()
        self.main_app_widget.chat_display.clear()
        self.main_app_widget.question_input.clear()
        self.login_widget.password_input.clear()
        self.login_widget.status_label.setText("성공적으로 로그아웃되었습니다.")
        self.stacked_widget.setCurrentWidget(self.login_widget)

    def signup(self, email, password):
        try:
            response = requests.post(
                f"{self.server_url}/signup",
                json={"email": email, "password": password}
            )
            if response.status_code == 200:
                self.login_widget.status_label.setText("회원가입 성공! 이제 로그인하세요.")
            else:
                self.login_widget.status_label.setText(response.json().get('detail', '회원가입 실패'))
        except requests.RequestException as e:
            self.login_widget.status_label.setText(f"서버 연결 오류: {e}")

    def load_sessions(self):
        """**신규: 서버에서 사용자의 세션 목록을 불러옴**"""
        if not self.user_id:
            return
        try:
            response = requests.get(f"{self.server_url}/sessions?user_id={self.user_id}")
            response.raise_for_status()
            sessions = response.json()
            
            self.main_app_widget.session_list.clear()
            if not sessions:
                self.main_app_widget.chat_display.setText("진행중인 세션이 없습니다.\n새로운 PDF로 채팅을 시작해보세요.")
                return

            for session in sessions:
                item = QListWidgetItem(session['session_title'])
                item.setData(Qt.ItemDataRole.UserRole, session['session_id'])
                self.main_app_widget.session_list.addItem(item)
            
            # 가장 최근 세션을 자동으로 선택
            if self.main_app_widget.session_list.count() > 0:
                self.main_app_widget.session_list.setCurrentRow(0)

        except requests.RequestException as e:
            self.main_app_widget.chat_display.setText(f"[오류] 세션 목록 로딩 실패: {e}")

    def start_new_session(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "PDF 파일 선택", "", "PDF Files (*.pdf)")
        if file_path:
            self.upload_and_create_session(file_path)
            
    def upload_and_create_session(self, file_path):
        filename = os.path.basename(file_path)
        self.main_app_widget.chat_display.setText(f"'{filename}' 업로드 및 처리 중...")
        QApplication.processEvents()
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (filename, f, 'application/pdf')}
                response = requests.post(
                    f"{self.server_url}/sessions/create_with_pdf?user_id={self.user_id}", 
                    files=files, 
                    timeout=300
                )
            
            response.raise_for_status()
            # 세션 목록을 새로고침하여 새 세션을 포함시킴
            self.load_sessions()

        except requests.RequestException as e:
            self.main_app_widget.chat_display.setText(f"세션 생성 실패: {e}")

    def session_selected(self, current, previous):
        """세션 선택 시, 이전 대화 기록을 불러옴"""
        if current:
            self.current_session_id = current.data(Qt.ItemDataRole.UserRole)
            self.load_chat_history(self.current_session_id) # **수정: 채팅 기록 로드**

    def load_chat_history(self, session_id):
        """**신규: 특정 세션의 대화 기록을 서버에서 불러옴**"""
        self.main_app_widget.chat_display.clear()
        try:
            response = requests.get(f"{self.server_url}/sessions/{session_id}/history")
            response.raise_for_status()
            history = response.json()

            if not history:
                self.main_app_widget.chat_display.setText("이전 대화 기록이 없습니다.\n질문을 입력하세요.")
                return

            for log in history:
                self.main_app_widget.chat_display.append(f"나: {log['user_question']}\n")
                self.main_app_widget.chat_display.append(f"봇: {log['model_answer']}\n")

        except requests.RequestException as e:
            self.main_app_widget.chat_display.setText(f"[오류] 대화 기록 로딩 실패: {e}")


    def ask_question(self):
        if not self.current_session_id:
            self.main_app_widget.chat_display.append("\n[오류] 먼저 세션을 선택하거나 생성해주세요.")
            return
            
        question = self.main_app_widget.question_input.text().strip()
        if not question:
            return
            
        self.main_app_widget.chat_display.append(f"나: {question}\n")
        self.main_app_widget.question_input.clear()
        QApplication.processEvents()

        try:
            payload = {"question": question, "session_id": self.current_session_id}
            response = requests.post(f"{self.server_url}/ask", json=payload, timeout=60)
            response.raise_for_status()
            answer = response.json().get("answer", "답변 없음")
            self.main_app_widget.chat_display.append(f"봇: {answer}\n")
        except requests.RequestException as e:
            self.main_app_widget.chat_display.append(f"\n[오류] 서버 통신 실패: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RAGClientApp()
    ex.show()
    sys.exit(app.exec())
