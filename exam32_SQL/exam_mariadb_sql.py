import pymysql
import pandas as pd

if __name__ == '__main__':
    my_db = pymysql.connect(
        user='root',
        passwd='1q2w3e4r',
        host='127.0.0.1',
        port=3306,
        db='shopdb',
        charset='utf8'
    )
    cursor = my_db.cursor((pymysql.cursors.DictCursor))
    sql = 'select * from buytbl where userID = "KHD"'
    cursor.execute(sql)  # 여기에 sql문을 입력한다.
    resp = cursor.fetchall()  # 서버에서 돌아오는 응답을 받는다.
    my_db.close()  # 반드시 끊어줘야 한다.
    print(resp)
    df = pd.DataFrame(resp)
    print(df)
    df.info()
    print(df.describe())