import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    """
    로컬 MySQL 데이터베이스의 연결, 테이블 생성, 데이터 CRUD 작업을 전담하는 클래스.
    """
    def __init__(self):
        # 로컬 MySQL 접속 정보 (사용자 환경에 맞게 수정)
        self.db_config = {
            'host': "localhost",
            'user': "root",
            'password': "your_local_password", # 로컬 MySQL 비밀번호
            'port': 3306
        }
        self.database_name = "rag"
        self._ensure_database_exists()

    def _get_connection(self, db_name=None):
        """데이터베이스 연결을 생성하는 내부 메서드"""
        config = self.db_config.copy()
        if db_name:
            config['database'] = db_name
        return mysql.connector.connect(**config)

    def _ensure_database_exists(self):
        """'rag' 데이터베이스가 없으면 생성합니다."""
        try:
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"'{self.database_name}' 데이터베이스가 준비되었습니다.")
        except Error as e:
            print(f"데이터베이스 확인 중 오류 발생: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        # 'rag' 데이터베이스를 기본 연결 설정에 추가
        self.db_config['database'] = self.database_name

    def execute_query(self, query, params=None, fetch=None):
        """일반 쿼리 실행을 위한 범용 메서드"""
        connection = None
        result = None
        try:
            connection = self._get_connection(self.database_name)
            cursor = connection.cursor(dictionary=True if fetch else False) # 조회 시 딕셔너리로 결과 받기
            cursor.execute(query, params or ())
            
            if fetch == 'one':
                result = cursor.fetchone()
            elif fetch == 'all':
                result = cursor.fetchall()
            else:
                connection.commit()
                result = cursor.lastrowid # INSERT 시 마지막 ID 반환
        except Error as e:
            print(f"쿼리 실행 중 오류 발생: {e}")
            if connection:
                connection.rollback()
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
        return result

    def setup_tables(self):
        """RAG 서비스에 필요한 모든 테이블을 순서대로 생성합니다."""
        queries = [
            # 1. Users 테이블
            """
            CREATE TABLE IF NOT EXISTS Users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            # 2. Documents 테이블
            """
            CREATE TABLE IF NOT EXISTS Documents (
                document_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                file_name VARCHAR(255) NOT NULL,
                file_path VARCHAR(512) NOT NULL UNIQUE,
                status ENUM('업로드중', '처리중', '완료', '실패') NOT NULL DEFAULT '업로드중',
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
            );
            """,
            # 3. Sessions 테이블
            """
            CREATE TABLE IF NOT EXISTS Sessions (
                session_id VARCHAR(36) PRIMARY KEY,
                user_id INT NOT NULL,
                document_id INT NULL,
                session_title VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (document_id) REFERENCES Documents(document_id) ON DELETE SET NULL
            );
            """,
            # 4. Document_Chunks 테이블
            """
            CREATE TABLE IF NOT EXISTS Document_Chunks (
                chunk_id INT AUTO_INCREMENT PRIMARY KEY,
                document_id INT NOT NULL,
                vector_id VARCHAR(255) NOT NULL UNIQUE,
                INDEX (vector_id),
                FOREIGN KEY (document_id) REFERENCES Documents(document_id) ON DELETE CASCADE
            );
            """,
            # 5. QnA_Logs 테이블
            """
            CREATE TABLE IF NOT EXISTS QnA_Logs (
                qna_id INT AUTO_INCREMENT PRIMARY KEY,
                session_id VARCHAR(36) NOT NULL,
                user_question TEXT NOT NULL,
                model_answer MEDIUMTEXT NOT NULL,
                retrieved_context MEDIUMTEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES Sessions(session_id) ON DELETE CASCADE
            );
            """
        ]
        
        for query in queries:
            self.execute_query(query)
        print("모든 테이블이 성공적으로 설정되었습니다.")
