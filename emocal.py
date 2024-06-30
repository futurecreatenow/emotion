from fer import FER
import matplotlib.pyplot as plt
import sys
import json
import os
import numpy as np
import pandas as pd
import pymysql



def get_mysql(host,user,password,database,table):
    # データベースに接続
    connection = pymysql.connect(host=host,
                                user=user,
                                password=password,
                                database=database,
                                cursorclass=pymysql.cursors.DictCursor)
    # mysqlに格納されているデータを全て抽出
    mysql_exist = []

    try:
        with connection.cursor() as cursor:
            #データの取得・表示
            cursor.execute("SELECT * FROM " + table + ";")
            mysql_exist = cursor.fetchall()
            print("#############################################")
            print("#################  MYSQL_DATA ###############")
            print("\n")
            print(mysql_exist)
            print("\n")
            print("#############################################")
            print("#############################################")
            return mysql_exist
    finally:
        connection.close()


def get_df(emotion_data):
    # pandasでデータベース化
    df = pd.DataFrame(emotion_data)
    print(df)