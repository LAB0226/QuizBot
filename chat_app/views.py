# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from richmenu import RichMenu
from richmenu import RichMenuManager

import requests
import json
import logging

#----------------------------------
# リッチメニューの表示処理
#----------------------------------
def richmenu_regist(user_id):
    channel_access_token = settings.LINE_ACCESS_TOKEN
    rmm = RichMenuManager(channel_access_token)
    rm = RichMenu(name="Test menu", chat_bar_text="Open this menu")
    rm.add_area(551, 325, 321, 321, "message", "up")
    rm.add_area(876, 651, 321, 321, "message", "right")
    rm.add_area(225, 651, 321, 321, "message", "left")
    rm.add_area(551, 972, 321, 321, "message", "down")
    rm.add_area(1907, 657, 367, 367, "message", "btn a")
    rm.add_area(1433, 657, 367, 367, "message", "btn b")
    res = rmm.register(rm, "/home/ec2-user/QuizBot/chat_app/test_richmenu.png")
    richmenu_id = res["richMenuId"]
    print("***** Registered as " + richmenu_id)
    rmm.apply(user_id,richmenu_id)

#-----------------------------
#----------------------------------
# 動作確認用
#----------------------------------
def index(request):
    return HttpResponse("This is bot api.")

#----------------------------------
# LINE APIからのメッセージを受ける処理
#----------------------------------
def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得
    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']   # typeの取得

        if message_type == 'text':
            text = e['message']['text']    # 受信メッセージの取得
            reply += reply_text(reply_token, text)   # LINEにセリフを送信する関数
    richmenu_regist(request_json['events'][0]['source']['userId'])
    print(request_json)
    return HttpResponse(reply)  # テスト用

#----------------------------
# LINE_APIに返事を送る
#----------------------------
REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + settings.LINE_ACCESS_TOKEN,
    "method": "POST"
}

def reply_text(reply_token, text):
    reply = text + "...!?"
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": reply
                }
            ]
    }
    
    logging.debug(HEADER)

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return reply
