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
            'password': "minjae0327", # 로컬 MySQL 비밀번호
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
        
        
        #-----------------------------------------------------------
        # db 조작 기능
        #-----------------------------------------------------------
        
        def check_table_data(self, table_name):
            """데이터베이스에 특정 테이블에 저장된 데이터를 조회하여 확인합니다."""
            connection = None
            cursor = None
            
            try:
                connection = mysql.connector.connect(**self.db_config)
                cursor = connection.cursor()
                
                # 데이터 조회 쿼리만 실행
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()
                
                if not rows:
                    print("테이블에 데이터가 없습니다.")
                else:
                    column_name = [decs[0] for decs in cursor.description]
                    
                    print(f"\n--- '{table_name}' 테이블 데이터 ---")
                    for row in rows:
                        record_details = []
                        # 4. 컬럼명과 값을 zip으로 묶어서 '컬럼명: 값' 형태로 만들기
                        for col_name, value in zip(column_name, row):
                            record_details.append(f"{col_name}: {value}")
                            
                        print("\n".join(record_details))
                        

                print("---------------------------------")

            except Error as e:
                print(f"오류 발생: {e}")
            finally:
                if connection and connection.is_connected():
                    if cursor:
                        cursor.close()
                    connection.close()
                    print("\n연결이 종료되었습니다.")



    def check_tables_in_db(self):
        """데이터베이스에 접속하여 테이블 목록을 출력합니다."""
        connection = None
        cursor = None
        
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            # 'rag' 데이터베이스에 있는 모든 테이블 목록을 보여주는 SQL 쿼리
            cursor.execute("SHOW TABLES;")
            
            tables = cursor.fetchall()
            
            if tables:
                print("\n[테이블 목록]")
                for table in tables:
                    print(f"- {table[0]}")
            else:
                print("\n데이터베이스에 테이블이 없습니다.")

        except Error as e:
            print(f"오류가 발생했습니다: {e}")

        finally:
            if connection and connection.is_connected():
                if cursor:
                    cursor.close()
                connection.close()
                print("\n연결이 종료되었습니다.")
                
                
        
    def insert_data(self, table_name, data_dict):
        """
        특정 테이블에 딕셔너리 형태의 데이터를 삽입합니다.
        내부적으로 INSERT 쿼리를 동적으로 안전하게 생성합니다.
        
        :param table_name: 데이터를 삽입할 테이블 이름 (예: "products")
        :param data_dict: 삽입할 데이터. {'컬럼명': 값} 형태의 딕셔너리
        """
        connection = None
        cursor = None
        
        if not data_dict or not isinstance(data_dict, dict):
            print("삽입할 데이터가 없거나, 데이터 형식이 딕셔너리가 아닙니다.")
            return

        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()

            # 1. 딕셔너리에서 컬럼명 리스트와 값 리스트를 분리합니다.
            columns = data_dict.keys()
            values = data_dict.values()
            
            # 2. 컬럼명과 플레이схолдер 부분을 동적으로 생성합니다.
            # 컬럼명은 백틱(`)으로 감싸주어 예약어와 충돌을 방지합니다.
            formatted_columns = f"({', '.join([f'`{col}`' for col in columns])})"
            placeholders = f"({', '.join(['%s'] * len(values))})"
            
            # 3. 최종 INSERT 쿼리 문자열을 조립합니다.
            query = f"INSERT INTO {table_name} {formatted_columns} VALUES {placeholders}"

            # print(f"생성된 쿼리: {query}") # 디버깅용: 실제 실행될 쿼리 확인

            # 4. 쿼리 실행 (값은 반드시 튜플 형태로 전달)
            cursor.execute(query, tuple(values))
            
            # 5. 변경 사항을 데이터베이스에 최종 적용(커밋)
            connection.commit()
            
            print(f"\n'{table_name}' 테이블에 데이터가 성공적으로 삽입되었습니다.")
            print(f"삽입된 행의 ID: {cursor.lastrowid}")

        except Error as e:
            print(f"오류가 발생했습니다: {e}")
        finally:
            if connection and connection.is_connected():
                if cursor:
                    cursor.close()
                connection.close()
                print("\n연결이 종료되었습니다.")    



    def drop_table(self, table_name):
        """데이터베이스에 접속하여 지정된 테이블을 삭제합니다."""
        connection = None
        cursor = None
        
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            # 지정된 테이블을 삭제하는 SQL 쿼리
            # 'IF EXISTS'를 사용하여 테이블이 없을 때 오류가 발생하는 것을 방지합니다.
            drop_query = f"DROP TABLE IF EXISTS {table_name}"
            
            cursor.execute(drop_query)
            
            # 변경 사항을 최종 적용(커밋)
            connection.commit()
            
            print(f"'{table_name}' 테이블이 성공적으로 삭제되었습니다.")

        except Error as e:
            print(f"오류가 발생했습니다: {e}")

        finally:
            if connection and connection.is_connected():
                if cursor:
                    cursor.close()
                connection.close()
                print("\n연결이 종료되었습니다.")
                
        
        
    def create_table(self, table_query):
        """데이터베이스에 새로운 테이블을 생성합니다."""
        connection = None
        cursor = None
        
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            # 데이터 조회 쿼리만 실행
            cursor.execute(table_query)
            
            print("테이블이 성공적으로 생성되었습니다.")

        except Error as e:
            print(f"오류 발생: {e}")
        finally:
            if connection and connection.is_connected():
                if cursor:
                    cursor.close()
                connection.close()
                print("\n연결이 종료되었습니다.")
