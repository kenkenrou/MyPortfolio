import os
import cv2
import glob

# 特徴量ファイルをもとに分類器を作成
classifier = cv2.CascadeClassifier('lbpcascade_animeface.xml')


# リストの全要素からreplaceしたい単語をreplaceする関数
# 第一引数: replaceするリスト  第二引数を第三引数にreplace  戻り値: 新しいリスト
def list_replace(list, old_word, new_word):
    new_list = []
    for temp in list:
        new_list.append(temp.replace(old_word, new_word))
    #print (new_list)
    return new_list

#
# "referent_path"フォルダ内に置いた画像から顔画像を検出し切り取るプログラム
# 画像から顔が検出された場合は"faces_output_dir"に切り取った顔画像を保存
# 画像から顔が検出されなかった場合は"non_face_output_dir"に元画像を保存
#

referent_path =  "./" + "picture" # 参照するデータのパス
faces_output_dir = "faces"
non_face_output_dir = "non_face"

picture_datapath = glob.glob(referent_path + "/*")  # referent_path下にある参照するデータリストのパス
picture_data = list_replace(picture_datapath, referent_path + "\\", "")  # referent_path下にある参照するデータリスト
# picture_datapath = "./OrigPicData\\74060_p0.png"
# picture_data = "74060_p0.png"


# フォルダ内にはJPEGとPNG以外置かないでください
# 顔の検出
for picture_name in picture_data:

    # picture_name = "sample.jpg"
    image = cv2.imread(referent_path + "/" + picture_name) # 画像読み込み(gifは非対応)

    picture_name = picture_name.replace(".jpg", "")
    picture_name = picture_name.replace(".png", "")

    # グレースケールで処理を高速化
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = classifier.detectMultiScale(gray_image)

    # 画像内に顔が検出されなかった場合-----------------------------------
    if len(faces) < 1: 
        print(picture_name + " : non face")
        # 検出されなかった画像のディレクトリを作成
        if not os.path.exists(non_face_output_dir):
            os.makedirs(non_face_output_dir)
        output_path = os.path.join(non_face_output_dir, picture_name + '.jpg')
        cv2.imwrite(output_path, image)

    # 顔が検出された場合-------------------------------------------------------------
    else :
        print(picture_name + " : have face")
        # 検出し切りっ取った顔画像ディレクトリを作成
        if not os.path.exists(faces_output_dir):
            os.makedirs(faces_output_dir)

        for i, (x, y, w, h) in enumerate(faces):
            # 一人ずつ顔を切り抜く
            face_image = image[y:y + h, x:x + w]
            temp = picture_name + "_" + str(i) + '.jpg'
            output_path = os.path.join(faces_output_dir, temp)
            cv2.imwrite(output_path, face_image)

        # cv2.imwrite('face.jpg', image) # 元画像
        """
        for x, y, w, h in faces:
            # 四角を描く
            cv2.rectangle(image, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=3)

        cv2.imwrite('faces.jpg', image) # 矩形で囲った画像
        """
    print("finish this picture named %s" % picture_name)

print("That's all.")
