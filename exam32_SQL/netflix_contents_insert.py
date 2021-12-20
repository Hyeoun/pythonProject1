import pandas as pd
import pymysql
import numpy as np

def insert(sql):
    conn = pymysql.connect(
        user='root',
        passwd='1q2w3e4r',
        host='127.0.0.1',
        port=3306,
        db='netflix',
        charset='utf8'
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()
    except:
        print('conn error')
    finally:
        conn.close()

df = pd.read_csv('../datasets/netflix_titles.csv')
print(df.head())
df.info()
df.fillna('', inplace=True)

for i in range(len(df)):
    a = []
    for j in range(12):
        if j != 7:
            a.append('null' if df.iloc[i, j] == '' else '"{}"'.format(df.iloc[i, j]))
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
    print(sql)

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

