def query_sql(query):
    import pymysql
    import pandas as pd

    conn = pymysql.connect(
            host="localhost", # MariaDB 서버 주소
            port=3306,
            user="webuser",       # 사용자명
            password="webuser",  # 비밀번호
            database="DDProject",  # 사용할 데이터베이스
            charset="utf8mb4",  # 한글 지원
            autocommit=False
        )

    try:
        with conn.cursor() as cursor:
            cursor.execute(query.strip())
            if query.strip().lower().startswith('select'):
                columns = [col[0] for col in cursor.description]
                result = cursor.fetchall()
                df = pd.DataFrame(result, columns = columns)
                if 'id' in df.columns:
                    df = df.set_index('id')
                return df
            else:
                conn.commit()

    except Exception as e:
        conn.rollback()  # ⚠ 예외 발생 시 트랜잭션 전체 롤백
        print(f"쿼리 실행 중 오류 발생: {e}")
    finally:
        conn.close()