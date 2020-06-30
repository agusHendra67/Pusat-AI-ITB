import os
import pandas as pd
from flask import Flask, request, abort
from flask.logging import create_logger 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
LOG = create_logger(app)

line_bot_api = LineBotApi('DhLYkk/1uuQ130naHtlK2g7ebRDqe+OB0rVIGgFXqyRTf3zOCNTdEwYkDbDNOYF7MJNgHK1T21nK7s3Mvy+VboMpODA9uC5LzvqdqzjmtXZrR7+LnA4Wc9RK/rqeKJAbjSVSpz9qbanDOLFJdx6qxwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('725f080ba14b01dd9e2f0f8022afd674')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    LOG.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    data = pd.DataFrame()
    msg = (event.message.text).lower()

    if ('hai' in msg) or ('hello' in msg) or ('hai' in msg) or ('hi' in msg) :
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hello pengguna!'))
    else :
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Terimakasih, tanggapan anda akan disimpan di sistem :)'))
        
    profile = line_bot_api.get_profile(event.user_id)
    #waktu 
    data['profile'] = profile
    data['komplain_teks'] = msg
    data.to_csv('Data Teks Komplain LINE')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)