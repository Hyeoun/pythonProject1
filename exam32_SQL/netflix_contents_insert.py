import pandas as pd
import pymysql
import numpy as np
import pickle

df = pd.read_csv('../datasets/netflix_titles.csv')
print(df.head())
df.info()

df.fillna('', inplace=True)

conn = pymysql.connect(
        user='root',
        passwd='1q2w3e4r',
        host='127.0.0.1',
        port=3306,
        db='netflix',
        charset='utf8'
    )
# with open('./errors.pickle', 'rb') as f:  # 에러났을때
#     error_list = pickle.load(f)
errors = []
for i in range(len(df)):  # 에러날때 range(len(df)) 대신 error_list를 넣는다.
    try:
        a = []
        for j in range(12):
            if j != 7:
                temp = df.iloc[i, j].replace("'", "\\\'")
                temp = temp.replace('"', '\\\"')
                a.append('null' if temp == '' else '"{}"'.format(temp))
            else:
                a.append(df.iloc[i, j])
        sql = 'insert into netflix_contents value({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});'.format(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11])
        # sql = 'insert into netflix_contents value({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});'.format(
        #     '"{}"'.format(df.iloc[i, 0]),
        #     '"{}"'.format(df.iloc[i, 1]),
        #     '"{}"'.format(df.iloc[i, 2]),
        #     'null' if df.iloc[i, 3] == '' else '"{}"'.format(df.iloc[i, 3]),
        #     'null' if df.iloc[i, 4] == '' else '"{}"'.format(df.iloc[i, 4]),
        #     'null' if df.iloc[i, 5] == '' else '"{}"'.format(df.iloc[i, 5]),
        #     'null' if df.iloc[i, 6] == '' else '"{}"'.format(df.iloc[i, 6]),
        #     df.iloc[i, 7],
        #     'null' if df.iloc[i, 8] == '' else '"{}"'.format(df.iloc[i, 8]),
        #     'null' if df.iloc[i, 9] == '' else '"{}"'.format(df.iloc[i, 9]),
        #     '"{}"'.format(df.iloc[i, 10]),
        #     '"{}"'.format(df.iloc[i, 11]))
        # print(sql)
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()
    except:
        print(sql)
        errors.append(i)
        print(i)

conn.close()
with open('./errors.pickle', 'wb') as f:  # 통신 에러 대비
    pickle.dump(errors, f)

# print(df.listed_in.head())
# print(df.type.unique())
# max_length = 0
# df_dir = df.description.dropna(inplace=False)
# for i in df_dir:
#     if max_length < len(i): max_length = len(i)
#
# # for i, year in enumerate(df_dir):
# #     if max_length < year:
# #         max_length = year
#
# print(max_length)

