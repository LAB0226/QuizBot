# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

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
ACCESS_TOKEN = 'uzvNY66qyX1+swPd8r1H+2AjgHHhlLJV/WXnz/HamUnm48zyOj7xg7J5jXY3tG3WIQBWBhkxffLs5jwdo2T8J4/FueB04eL3JzaZJyxIDCDxfee4P+lECThQbwOh4gGN8zpoya/VoknStuk7MiusMwdB04t89/1O/w1cDnyilFU='
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN,
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
#-----------------------------