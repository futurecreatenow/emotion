from fer import FER
import matplotlib.pyplot as plt
import sys
import json
import os
import numpy as np
import pandas as pd
import pymysql
import emofig
import emocal
import datetime
import time
import cv2

## 問題点
## 1)ビデオが再生されない
def video(video):
    cap = cv2.VideoCapture(video) #ビデオの設定
    cap_camera = cv2.VideoCapture(0) # カメラの設定
    video_kind = "me"
    count_cap = 0 # カウント用
    count_limit = 10 # カウントの閾値
    time_interval = 0.5 # 撮影間隔
    if (cap.isOpened()== False):  
        print("ビデオファイルを開くとエラーが発生しました") 

    while(cap.isOpened()):

        ret, frame = cap.read()
        if ret == True:
            cv2.imshow("Video", frame)                          

            # カメラでの撮影
            while cap_camera.isOpened():
                ret_camera,frame_camera = cap_camera.read()
                time_ = datetime.datetime.now()
                timestr = time_.strftime("%H%M%S")
                pic_path = f"./data/{video_kind + str(timestr)}.jpeg"
                cv2.imwrite(pic_path, frame_camera)
                count_cap += 1
                # 特定の間隔をおいて撮影する:単位は秒
                time.sleep(time_interval)
                if count_cap == count_limit:
                    break
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            if cv2.waitKey(25) & 0xFF == ord('q'): 
                break
        
        else:
            break

    # カメラとビデオを閉じる
    cap.release()
    cap_camera.release()
    cv2.destroyAllWindows()

def webcamera():
    cap = cv2.VideoCapture(0) # カメラCh.(ここでは0)を指定
    count = 3 # 画像の枚数
    count_cap = 0 # カウント用
    time_interval = 10 # 撮影間隔
    video_kind = 'relax' # 動画の種類や感情
    json_input = []

    # 画像をキャプチャする
    while cap.isOpened():
        ret, frame = cap.read()
        # 画像を保存する
        time_ = datetime.datetime.now()
        timestr = time_.strftime("%H%M%S")
        pic_path = f"./data/{video_kind + str(timestr)}.jpeg"
        cv2.imwrite(pic_path, frame)
        json_input.append(pic_path)
        count_cap += 1

        # 特定の間隔をおいて撮影する:単位は秒
        time.sleep(time_interval)
        if count_cap == count:
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # カメラを閉じる
    cap.release()
    cv2.destroyAllWindows()

    # jsonファイルへの書き込み
    print(json_input)



def emotion_cap(pic):
    # 画像の取得
    test_image_one = plt.imread(pic)
    emo_detector = FER(mtcnn=True)
    captured_emotion = emo_detector.detect_emotions(test_image_one)

    INITDATA = 0
    EMOTIONS = {"angry":INITDATA,"disgust":INITDATA,"fear":INITDATA, "happy":INITDATA, "sad":INITDATA, "surprise":INITDATA,"neutral":INITDATA}

    # 全ての感情の取得
    try:
        for key in EMOTIONS.keys():
            if captured_emotion[0]['emotions'][key]:
                EMOTIONS[key] = captured_emotion[0]['emotions'][key]
    except IndexError:
        print('顔を検知できませんでした')

    return EMOTIONS

def mysql_insert(dic):
    # データベースに接続
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='Suika628',
                                database='emotion',
                                cursorclass=pymysql.cursors.DictCursor)
    # mysqlに格納されているデータを全て抽出
    mysql_exist = []
    # 主キーのみ抽出
    mysql_name = []
    try:
        with connection.cursor() as cursor:
            #データの取得・表示
            cursor.execute("SELECT * FROM " + TABLE + ";")
            mysql_exist = cursor.fetchall()
            print("\n")
            print("#############################################")
            print("############# before MYSQL_DATA #############")
            print("\n")
            print(mysql_exist)
            print("\n")
            print("#############################################")
            print("#############################################")
            print("\n")

            # mysqlの重複をなくす
            for i in mysql_exist:
                mysql_name.append(i['name'])
                mysql_name = list(set(mysql_name))

            for key in dic:
                # 既に存在する主キーのデータはinsertしない
                if key in mysql_name:
                    continue
                # 存在しない主キーのデータはinsertする
                else:
                    print("\n")
                    print("#########   data insert   ##########")
                    print(f"data name >>>{key}")
                    sql = f"INSERT INTO info(name,angry,disgust,fear,happy,sad,surprise,neutral) values ('{key}',{dic[key]['angry']},{dic[key]['disgust']},{dic[key]['fear']},{dic[key]['happy']},{dic[key]['sad']},{dic[key]['surprise']},{dic[key]['neutral']});"
                    cursor.execute(sql)
                    connection.commit()


            #最新データの取得
            cursor.execute("SELECT * FROM " + TABLE + ";")
            mysql_exist = cursor.fetchall()
            print("#############################################")
            print("############## after MYSQL_DATA #############")
            print("\n")
            print(mysql_exist)
            print("\n")
            print("#############################################")
            print("#############################################")
            return mysql_exist
    finally:
        connection.close()

if __name__ == '__main__':
    ## データを挿入したい場合は1、データを解析したい場合は2、カメラで画像を取得したい場合は3,dataフォルダのデータをjsonに追加したい場合4,
    ## MYSQLデータを整理したい場合は5、特定のビデオを閲覧して画像を取得したい場合6
    select_option = 6

    # mysql情報
    HOST='localhost'
    USER='root'
    PASSWORD='Suika628'
    DATABASE='emotion'
    TABLE = 'info'

    # 感情
    ANGRY = "angry"
    DISGUST = "disgust"
    FEAR = "fear"
    HAPPY = "happy"
    SAD = "sad"
    SURPRISE = "surprise"
    NEUTRAL = "neutral"
    EMOTIONS_LIST = [ANGRY,DISGUST,FEAR,HAPPY,SAD,SURPRISE,NEUTRAL]

    # データベースに挿入する
    if select_option == 1:
        # 第一引数は設定ファイル
        json_file = sys.argv[1]
        json_file = open(json_file,'r')
        json_data = json.load(json_file)
        
        # 感情の値を格納する辞書型
        emotion_dict = {}

        # 画像を一枚ずつ読み込み感情の値を取得
        for i in json_data["picture"].values():
            pic = i
            emotion_result = emotion_cap(pic)
            filename = os.path.basename(pic)
            emotion_dict[filename] = emotion_result
        print(emotion_dict)

        ## 感情を円グラフにする
        # emofig.emotion_show(EMOTIONS_LIST,emotion_dict)

        ## mysqlへデータを格納する
        mysql_insert(emotion_dict)


    # データを解析する
    elif select_option == 2:
        # データベース情報を一括取得
        emotions_analysis_data = emocal.get_mysql(HOST,USER,PASSWORD,DATABASE,TABLE)

        ## pandasでデータベース化する
        # emocal.get_df(emotions_analysis_data)

    elif select_option == 3:
        # webカメラから画像を取得して保存する
        webcamera()
        # jsonに書き込みする
        json_file = sys.argv[1]
        emofig.json_write(json_file)

    # jsonファイルにない画像ファイルのみをjsonの辞書型に追加する
    elif select_option == 4:
        json_file = sys.argv[1]
        emofig.json_write(json_file)

    # jsonファイルに記載のないのデータをMYSQLから削除する
    elif select_option == 5:
        json_file = sys.argv[1]
        emofig.mysql_delete(json_file,HOST,USER,PASSWORD,DATABASE,TABLE)

    # videoを再生してcameraを起動する
    elif select_option == 6:
        video_path = f"./video/test2.mp4"
        # json_file = sys.argv[1]
        video(video_path)
