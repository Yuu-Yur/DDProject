def query_sql(query):
    import pymysql
    import pandas as pd

    conn = pymysql.connect(
            host="localhost", # MariaDB 서버 주소
            port=3306,
            user="webuser",       # 사용자명
            password="webuser",  # 비밀번호
            database="DDProject",  # 사용할 데이터베이스
            charset="utf8mb4"  # 한글 지원
        )

    try:
        with conn.cursor() as cursor:
            sql = query
            cursor.execute(sql)

            columns = [col[0] for col in cursor.description]
            result = cursor.fetchall()
        df = pd.DataFrame(result, columns = columns)
        if 'id' in df.columns:
            df = df.set_index('id')
        return df
    finally:
        conn.close()