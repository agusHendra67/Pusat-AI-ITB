import os
import re
from datetime import datetime
import pytz

from flask import Flask, request, abort, jsonify
from flask.logging import create_logger 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

import psycopg2

#DATABASE Connection
connection = psycopg2.connect(user="uigronqdtlgfgy",
                              password="a35b4e9e8ed6798ee17180222a67fd77fe9109fac5163cefd5b20ac405894e96",
                              host="ec2-52-207-25-133.compute-1.amazonaws.com",
                              port="5432",
                              database="d9npil276i06um")
cursor = connection.cursor()

#app
app = Flask(__name__)
LOG = create_logger(app)

#line API
line_bot_api = LineBotApi('DhLYkk/1uuQ130naHtlK2g7ebRDqe+OB0rVIGgFXqyRTf3zOCNTdEwYkDbDNOYF7MJNgHK1T21nK7s3Mvy+VboMpODA9uC5LzvqdqzjmtXZrR7+LnA4Wc9RK/rqeKJAbjSVSpz9qbanDOLFJdx6qxwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('725f080ba14b01dd9e2f0f8022afd674')

#Route
@app.route("/callback", methods=['GET','POST'])
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

#Even saat user mem-follow akun PusatAI ITB    
@handler.add(FollowEvent)
def handle_message_follow(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Halo {} selamat datang di Chatbot ITB Care, silakan pilih menu (1/2/3/4/5/6) sbb:\n1. Penyampaian masukan untuk ITB\n2. Tanya informasi fasilitas Sarana Prasarana di ITB \n3. Tanya informasi mengenai Sabuga ITB\n4. Tanya informasi perpustakaan ITB\n5. Tanya informasi Pelayanan Kesehatan ITB\n6. Online booking fasilitas'.format(profile.display_name)))

#Even saat user mengklik button
@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == "1":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Silahkan masukkan keluhan anda'))
    elif event.postback.data == "2" :
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Silahkan masukkan lokasi'))
    elif event.postback.data == "3":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Silahkan masukkan data gambar'))
    
#Even saat user mengirim pesan
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #teks 
    msg = (event.message.text).lower()
    #user profile
    profile = line_bot_api.get_profile(event.source.user_id)
    #nama gedung kuliah
    gdg_kuliah = ['labtek','lfm', 'oktagon', 'tvst', 'gku', 'gku barat', 'gku timur', 'labtek v', 'labtek 5', 'labtek vi', 'labtek 6', 'labtek i', 'labtek 1', 'bsc', 'gedung doping', 'doping', 'crcs', 'cas', 'cadl']
    
    if msg == "1":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Silahkan masukkan email'))  
    elif re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+\.[a-z]+",msg) or re.findall(".com$", msg) or re.findall(".co.id$", msg) or re.findall(".org$", msg):
        buttons_template = ButtonsTemplate( 
        text='Halo {}, silahkan isi data dibawah ya :) *wajib'.format(profile.display_name),
        thumbnail_image_url='https://cdn.idntimes.com/content-images/community/2017/09/itb-d41de4ef55a5584eb4de86cdd085cc2d_600x400.jpg', 
        actions=[
            PostbackAction(label='Komplain*', data='1'),
            PostbackAction(label='Lokasi*', data='2'),
            PostbackAction(label='Foto/gambar', data='3'),
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

        #insert data into database
        postgres_insert_query = """ INSERT INTO public.user_profile (user_id, "line_displayName", email) VALUES (%s,%s,%s)"""
        record_to_insert = (event.source.user_id, profile.display_name, msg)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()  
    elif len(msg) <=7 and msg not in gdg_kuliah:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Selamat datang di Chatbot ITB Care, silakan pilih menu (1/2/3/4/5/6) sbb:\n1. Penyampaian masukan untuk ITB\n2. Tanya informasi fasilitas Sarana Prasarana di ITB \n3. Tanya informasi mengenai Sabuga ITB\n4. Tanya informasi perpustakaan ITB\n5. Tanya informasi Pelayanan Kesehatan ITB\n6. Online booking fasilitas'))
    else :
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Terimakasih atas waktunya, data berhasil disimpan'))

        #lokasi
        a = ["0"]
        for i in range(len(gdg_kuliah)):
            x = re.search(gdg_kuliah[i], msg)
            if x == None:
                pass
            else:
                a[0] = gdg_kuliah[i]
        lokasi = a[0]

        #waktu
        waktu = (datetime.fromtimestamp(event.timestamp/1e3).astimezone(tz= pytz.timezone('Asia/Jakarta'))).strftime("%m/%d/%Y, %H:%M:%S")

        #insert data into database
        postgres_insert_query = """ INSERT INTO public.komplain (user_id, message_id, teks_komplain, lokasi, waktu_komplain) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (event.source.user_id, event.message.id, msg, lokasi, waktu)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        
#  Even saat user mengirim pesan gambar           
@handler.add(MessageEvent, message=(ImageMessage))
def handle_message_image(event):

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Terimakasih atas waktunya, gambar berhasil disimpan'))

    
    # #get image as binary 
    # r = requests.get('https://api-data.line.me/v2/bot/message/{}/content'.format(event.message.id), headers={'Authorization' : 'Bearer DhLYkk/1uuQ130naHtlK2g7ebRDqe+OB0rVIGgFXqyRTf3zOCNTdEwYkDbDNOYF7MJNgHK1T21nK7s3Mvy+VboMpODA9uC5LzvqdqzjmtXZrR7+LnA4Wc9RK/rqeKJAbjSVSpz9qbanDOLFJdx6qxwdB04t89/1O/w1cDnyilFU='} )
    # img = r.content

    # #waktu
    # waktu = (datetime.fromtimestamp(event.timestamp/1e3).astimezone(tz= pytz.timezone('Asia/Jakarta'))).strftime("%m/%d/%Y, %H:%M:%S")

    
    # #insert image into database
    # postgres_insert_query = """ INSERT INTO public.komplain (user_id, message_id, waktu_komplain, gambar) VALUES (%s,%s,%s,%s)"""
    # record_to_insert = (event.source.user_id, event.message.id, waktu, img)
    # cursor.execute(postgres_insert_query, record_to_insert)
    # connection.commit()

        

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)