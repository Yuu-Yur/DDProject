#%%
import pandas as pd
import pymysql

# transactional
def insert_db(table_name,c_query,i_query,data_path):
    # DB 연결
    conn = pymysql.connect(
        host="localhost", # MariaDB 서버 주소
        port=3306,
        user="webuser",       # 사용자명
        password="webuser",  # 비밀번호
        database="DDProject",  # 사용할 데이터베이스
        charset="utf8mb4"  # 한글 지원
    )
    conn.autocommit(False)
    cursor = conn.cursor()
    try:
        # 테이블 크리에이트
        create_table_sql = f"""{c_query}"""

        cursor.execute(create_table_sql)



        # 1. 데이터 로드
        df = pd.read_csv(data_path, encoding='utf-8', header=0)
        # 2. 데이터 변환

        # 3. 날짜 변환 (문자열 → DATETIME)

        # 테이블 인서트
        placeholders = ', '.join(['%s'] * df.columns.values.size)
        insert_sql = f"""
            {i_query} VALUES ({placeholders})
        """

        data = df[df.columns.values].itertuples(index=False, name=None)
        cursor.executemany(insert_sql, data)
        # 변경 사항 저장
        conn.commit()
        print('커밋완료')

        #transactional error
    except pymysql.MySQLError as e:
        drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
        cursor.execute(drop_table_query)
        conn.rollback()
        print(e)
    finally:
        # 연결 종료
        cursor.close()
        conn.close()