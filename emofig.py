from pathlib import Path
import os
import itertools
import glob
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime

'''
概要:dataフォルダの画像を全てjsonについかする
関数名:json_write
引数：書き込むjsonファイルのパス
'''
def json_write(json_file):
    # jsonファイルの読み込み
    with open (json_file,'r') as file:
        data = json.load(file)
    data_original = dict(data)

    # 画像フォルダの画像ファイルの絶対パスを全て取得する
    pic_foleder = data_original["pic_foleder"] # 画像ファイルの格納フォルダパス
    file_path_lists = glob.glob("{}/**".format(pic_foleder), recursive=True)
    folder_path_lists = []
    for file_path in file_path_lists:
        print(file_path)
        if (os.path.isdir(file_path)):
            folder_path_lists.append(file_path)
    print(file_path_lists)

    # jsonファイルにない画像ファイルのみを追加する
    for path in file_path_lists:
        if '.jpeg' in path or '.jpg' in path:
            key_pic_file = Path(path).stem
            
            # jsonファイルにはない画像ファイル
            if not key_pic_file in data_original['picture']:
                print(key_pic_file)
        else:
            print("not append")



## 練習用:jsonファイルへの追加方法
def pra(json_file):
    # jsoｎファイルへの書き込み
    input_list = {}
    for i in range(3):
        path = f"./data/{i}.jpeg"
        input_list[i] = path
    
    print("###########################")
    print("##############追加するデータ############")
    print(input_list)
    print("###########################")
    print("###########################")

    # jsonファイルの読み込み
    with open (json_file,'r') as file:
        data = json.load(file)
    data_original = dict(data)

    # 追加した画像のキーの存在確認
    for key,value in input_list.items():
        # 存在する>>>キーを追加しない
        if key in data_original['picture']:
            continue
        # 存在しない>>>キーを追加する
        else:
            data_original['picture'][str(key)] = value
    updated_json = json.dumps(data_original,indent=4)

    print("###########################")
    print("##############更新するデータ############")
    print(updated_json)
    print("###########################")
    print("##########################")

    with open(json_file,'w') as file:
        file.write(updated_json)
    return 0


## 感情を円グラフにする
def emotion_show(EMOTIONS_LIST,emotion_dict):
    # 全ての画像の感情値の出力
    print("########################################")
    print(emotion_dict)
    print("########################################")

    # DataFrameの作成
    df = pd.DataFrame(emotion_dict)
    print(df)

    # 円グラフの作成(１枚ずつ表示)
    for i in df.columns:
        x = df[i]
        fig, ax = plt.subplots()
        ax.pie(x, labels=EMOTIONS_LIST, autopct="%1.1f %%")
        plt.show()