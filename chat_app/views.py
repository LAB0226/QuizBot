# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from richmenu    import Richmenu, RichMenuManager

import requests
import json

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

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return reply

#----------------------------------
# リッチメニューの表示処理
#----------------------------------
  channel_access_token = settings.LINE_ACCESS_TOKEN
  rmm = RichMenuManager(channel_access_token)
  rm = RichMenu(name="Test menu", chat_bar_text="Open this menu")
    rm.add_area(551, 325, 321, 321, "message", "up")
    rm.add_area(876, 651, 321, 321, "message", "right")
    rm.add_area(225, 651, 321, 321, "message", "left")
    rm.add_area(551, 972, 321, 321, "message", "down")
    rm.add_area(1907, 657, 367, 367, "message", "btn a")
    rm.add_area(1433, 657, 367, 367, "message", "btn b")

#-----------------------------
