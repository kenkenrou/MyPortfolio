#!/usr/bin/env PYTHONIOENCODING=UTF-8 python3
# -*- coding: utf-8 -*-

from pixivpy3 import *
from time import sleep
import os

# Enter the Illustrator-Id
#FollowUserList = [<ダウンロードする絵師のID>, xxx, xxx]
FollowUserList = [177784, 1203800]

# regarding refresh token, please refer to <https://qiita.com/yuki_2020/items/759e639a4cecc0770758>
REFRESH_TOKEN = "xxxxxxxxxxxx"


for id_search in FollowUserList:

    # Log in to pixiv
    api = PixivAPI()
    api.auth(refresh_token=REFRESH_TOKEN)
    aapi = AppPixivAPI()

    # Maximum number of illustrations
    works=300

    illustrator_id = api.users_works(id_search, per_page=works)
    total_works = illustrator_id.pagination.total

    if works < total_works:
        total_works = works

    illust = illustrator_id.response[0]

    # 名前にディレクトリ名に含んではいけない文字("/","*")があるとエラーになるのでその処理
    illust.user.name = illust.user.name.replace("/", "_")
    illust.user.name = illust.user.name.replace("*", "_")

    # Filter by tag
    target_tag = []  # e.g. target_tag = ["Fate/GrandOrder","FGO","FateGO","Fate/staynight"]

    # Designation of download destination

    # デフォルトでは絵師の名前でフォルダが作成される
    saving_direcory_path = "./pixiv_images/" + illust.user.name + "_" + str(id_search) + "/"
    if not os.path.exists(saving_direcory_path):
        os.mkdir("./pixiv_images")
        os.mkdir(saving_direcory_path)
    separator = "------------------------------------------------------------"

    #Display information of illustrator and illustrations
    print("Illustrator: {}".format(illust.user.name))
    print("Works number: {}".format(total_works))
    print(separator)

    # Download
    for work_no in range(0, total_works):
        illust = illustrator_id.response[work_no]

        if len(list(set(target_tag)&set(illust.tags))) == 0 and target_tag != []:
            continue

        print("Now: {0}/{1}".format(work_no + 1, total_works))
        print("Title: {}".format(illust.title))

        if os.path.exists(saving_direcory_path+str(illust.id)+"_p0.png") or os.path.exists(saving_direcory_path+str(illust.id)+"_p0.jpg"):
            # When the illustration has already downloaded
            print("Title:"+str(illust.title)+" has already downloaded.")
            print(separator)
            sleep(1)
            continue

        # illustrations with more than one picture
        if illust.is_manga:
            work_info = api.works(illust.id)

            for page_no in range(0, work_info.response[0].page_count):
                page_info = work_info.response[0].metadata.pages[page_no]
                aapi.download(page_info.image_urls.large, saving_direcory_path)
                sleep(3)
        # illustrations with only one picture
        else:
            aapi.download(illust.image_urls.large, saving_direcory_path)
            sleep(3)
        print(separator)

    print("Download complete!　Thanks to {}!!".format(illust.user.name))

print("That's all!")
