import mysql.connector
from mysql.connector import Error


class DatabaseManager:
    def __init__(self):
        #RDS info
        self.host = "localhost" #mysql workbench에 연결할 때 썼던 그 aws엔드포인트입니다.
        self.port = 3306 #포트번호는 손대지않으셨다면 3306 고정
        self.username = "root" #rds 만드실 때 입력하셨던 이름
        self.database = "rag" #DB내에서 연결하고싶은 데이터베이스 이름입니다.
        self.password = "minjae0327"

        self.db_config = {
            'host': self.host,
            'user': self.username,
            'password': self.password,
            'database': self.database,
            'port': self.port
        }
        
        

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