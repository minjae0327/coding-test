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
                -- 사용자를 식별하는 고유 번호 (기본 키)

                email VARCHAR(255) NOT NULL UNIQUE,
                -- 로그인에 사용할 이메일 (반드시 필요, 중복 불가)

                password_hash VARCHAR(255) NOT NULL,
                -- 비밀번호 원문을 암호화하여 저장

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                -- 사용자 가입일
            );
            """,
            # 2. Documents 테이블
            """
            CREATE TABLE IF NOT EXISTS Documents (
                document_id INT AUTO_INCREMENT PRIMARY KEY,
                -- 각 문서를 식별하는 고유 번호

                user_id INT NOT NULL,
                -- 이 문서를 업로드한 사용자의 ID

                file_name VARCHAR(255) NOT NULL,
                -- 업로드된 원본 파일 이름 (예: "my_paper.pdf")

                file_path VARCHAR(512) NOT NULL UNIQUE,
                -- 파일이 실제 저장된 경로 (예: S3 경로). 중복될 수 없음

                status ENUM('업로드중', '처리중', '완료', '실패') NOT NULL DEFAULT '업로드중',
                -- 문서의 현재 처리 상태

                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                -- 문서 업로드 시점

                -- 외래 키 설정: user_id는 Users 테이블의 user_id를 참조
                -- ON DELETE CASCADE: 만약 Users 테이블에서 사용자가 삭제되면, 관련된 문서도 함께 삭제됨
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
            );
            """,
            # 3. Sessions 테이블
            """
            CREATE TABLE IF NOT EXISTS Sessions (
                session_id VARCHAR(36) PRIMARY KEY,
                -- 각 대화 세션을 식별하는 고유 ID (UUID 사용 권장)

                user_id INT NOT NULL,
                -- 이 세션을 소유한 사용자의 ID

                document_id INT NULL,
                -- 이 대화가 특정 문서를 기반으로 할 경우 해당 문서 ID (필수 아님)

                session_title VARCHAR(255) NOT NULL,
                -- 대화방 제목

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                -- 세션 생성 시점
                
                vector_store_path VARCHAR(512) NULL,
                -- 벡터스토어가 저장된 지점

                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                -- 마지막 대화가 오고 간 시점 (자동 업데이트)
                

                -- 외래 키 설정
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
                -- ON DELETE SET NULL: 참조하던 문서가 삭제되어도 대화 세션 기록은 남기고, document_id만 NULL로 변경
                FOREIGN KEY (document_id) REFERENCES Documents(document_id) ON DELETE SET NULL
            );
            """,
            # 4. QnA_Logs 테이블
            """
            CREATE TABLE IF NOT EXISTS QnA_Logs (
                qna_id INT AUTO_INCREMENT PRIMARY KEY,
                -- 각 질의응답 쌍의 고유 번호

                session_id VARCHAR(36) NOT NULL,
                -- 이 질의응답이 어느 세션에 속하는지 식별

                user_question TEXT NOT NULL,
                -- 사용자가 입력한 질문 원문

                model_answer MEDIUMTEXT NOT NULL,
                -- 언어 모델이 생성한 답변 내용 (길 수 있으므로 MEDIUMTEXT 사용)

                retrieved_context MEDIUMTEXT,
                -- 답변 생성 시 RAG가 참고한 문서 조각들의 내용 (디버깅 및 분석에 유용)

                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                -- 질의응답이 발생한 시점

                -- 외래 키 설정: 참조하던 세션이 삭제되면, 관련된 모든 질의응답 기록도 함께 삭제
                FOREIGN KEY (session_id) REFERENCES Sessions(session_id) ON DELETE CASCADE
            );
            """
        ]
                
        try:
            for query in queries:
                self.execute_query(query)
            print("모든 테이블이 성공적으로 설정되었습니다.")
        except Error as e:
            print(f"테이블 설정 중 오류 발생: {e}")

       
        
        
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
                
                
                
     # --- 새로 추가된 함수 ---
    def check_all_tables_data(self):
        """데이터베이스의 모든 테이블과 그 안의 모든 데이터를 조회하여 출력합니다."""
        print("\n===== 모든 테이블 데이터 조회 시작 =====")
        try:
            # 1. 모든 테이블 목록 가져오기
            tables = self.execute_query("SHOW TABLES;", fetch='all')
            
            if not tables:
                print("데이터베이스에 테이블이 없습니다.")
                return

            # 2. 각 테이블을 순회하며 데이터 조회 함수 호출
            for table in tables:
                # execute_query가 딕셔너리 리스트를 반환하므로, 첫 번째 키의 값을 테이블 이름으로 사용
                table_name = list(table.values())[0]
                self.check_table_data(table_name)
                
        except Error as e:
            print(f"오류 발생: {e}")
        finally:
            print("\n===== 모든 테이블 데이터 조회 완료 =====")



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
                
                
    #------------------------------------------------------------
    #   모든 데이터 삭제 함수 
    #------------------------------------------------------------    
    def clear_all_data_from_tables(self):
        """
        데이터베이스의 모든 테이블 구조는 유지한 채, 모든 데이터만 삭제(TRUNCATE)합니다.
        외래 키 제약 조건을 처리하기 위해 일시적으로 비활성화 후 다시 활성화합니다.
        """
        connection = None
        cursor = None
        print("\n===== 모든 테이블의 데이터 삭제를 시작합니다... =====")
        
        try:
            connection = self._get_connection(self.database_name)
            cursor = connection.cursor()

            # 1. 외래 키 제약 조건 비활성화 (TRUNCATE 실행을 위해 필수)
            print("외래 키 제약 조건을 임시로 비활성화합니다.")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

            # 2. 모든 테이블 목록 가져오기
            cursor.execute("SHOW TABLES;")
            tables = [table[0] for table in cursor.fetchall()]

            # 3. 각 테이블을 순회하며 TRUNCATE 실행
            if tables:
                for table_name in tables:
                    print(f" -> '{table_name}' 테이블의 데이터를 삭제합니다.")
                    cursor.execute(f"TRUNCATE TABLE `{table_name}`;")
                print("\n모든 테이블의 데이터가 성공적으로 삭제되었습니다.")
            else:
                print("데이터베이스에 테이블이 없습니다.")

        except Error as e:
            print(f"데이터 삭제 중 오류가 발생했습니다: {e}")
        
        finally:
            # 4. 오류 발생 여부와 관계없이, 반드시 외래 키 제약 조건을 다시 활성화
            if connection and connection.is_connected():
                print("외래 키 제약 조건을 다시 활성화합니다.")
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
                cursor.close()
                connection.close()
            print("===== 데이터 삭제 작업 완료 =====")
