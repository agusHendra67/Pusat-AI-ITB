import os
import re
from datetime import datetime
import pytz
import requests

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
connection = psycopg2.connect(user="pzssbtkzpmnvub",
                              password="a772ca28135d8bfac88c7acd3b7d45f57f7a1d3b7498e5ddd66f4f5d4cc998dc",
                              host="ec2-54-91-178-234.compute-1.amazonaws.com",
                              port="5432",
                              database="d9h0giveuhud7e")
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
    #list of locations
    loc = open("gedung kuliah.txt", "r").read().splitlines()
    
    #insert profile data into database
    try :
        postgres_insert_query = """ INSERT INTO public.user_profile (user_id, "Line_displayName") VALUES (%s,%s)"""
        record_to_insert = (event.source.user_id, profile.display_name)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()  
    except (Exception, psycopg2.Error):
        pass
    
    #cek email tidak boleh kosong
    connection.rollback()
    cursor.execute("SELECT * FROM public.user_profile WHERE user_id = %s", (event.source.user_id,))
    connection.commit()
    rows = cursor.fetchall()
    for row in rows:
        if row[2] == None:
            b = "0"
        else :
            b = "1"
    

    #reply messages
    if msg == "1" and b =="0":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Silahkan masukkan email'))
    elif msg == "1" and b == "1":
        buttons_template = ButtonsTemplate( 
        text='Halo, silahkan isi data dibawah ya :) *wajib diisi',
        thumbnail_image_url='https://cdn.idntimes.com/content-images/community/2017/09/itb-d41de4ef55a5584eb4de86cdd085cc2d_600x400.jpg', 
        actions=[
            PostbackAction(label='Komplain*', data='1'),
            PostbackAction(label='Lokasi', data='2'),
            PostbackAction(label='Foto/gambar', data='3'),
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    if msg == "6" and b =="0":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Belum ada email terdaftar, silahkan masukkan terlebih dahulu'))
    elif msg == "6" and b =="1":
        line_bot_api.reply_message(
            event.reply_token,
            [
             TextSendMessage(text='email aktif saat ini : {}'.format(row[2])),
             TextSendMessage(text='Ketikkan email yang baru')
            ])   
    elif len(msg) <=7 and msg not in loc:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Halo {}\nselamat datang di Chatbot ITB Care\nsilakan pilih menu (1/2/3/4/5/6) sbb:\n1. Penyampaian masukan untuk ITB\n2. Tanya informasi fasilitas Sarana Prasarana di ITB\n3. Tanya informasi mengenai Sabuga ITB\n4. Tanya informasi perpustakaan ITB\n5. Tanya informasi Pelayanan Kesehatan ITB\n6. Ganti email'.format(profile.display_name)
                            ))
    elif re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+\.[a-z]+",msg) and (b == "1") :
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='Email berhasil diganti'),
             TextSendMessage(text='Halo {}\nselamat datang di Chatbot ITB Care\nsilakan pilih menu (1/2/3/4/5/6) sbb:\n1. Penyampaian masukan untuk ITB\n2. Tanya informasi fasilitas Sarana Prasarana di ITB\n3. Tanya informasi mengenai Sabuga ITB\n4. Tanya informasi perpustakaan ITB\n5. Tanya informasi Pelayanan Kesehatan ITB\n6. Ganti email'.format(profile.display_name))
             ])
        
        #update changed email in database
        connection.rollback()
        postgres_update_query = """ UPDATE public.user_profile set email = %s where user_id = %s"""
        record_to_update = (msg, event.source.user_id)
        cursor.execute(postgres_update_query, record_to_update)
        connection.commit()  
    elif re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+\.[a-z]+",msg) or ((b == "1") and (msg == "1" or msg == "a")):
        buttons_template = ButtonsTemplate( 
        text='Halo, silahkan isi data dibawah ya :) *wajib diisi',
        thumbnail_image_url='https://cdn.idntimes.com/content-images/community/2017/09/itb-d41de4ef55a5584eb4de86cdd085cc2d_600x400.jpg', 
        actions=[
            PostbackAction(label='Komplain*', data='1'),
            PostbackAction(label='Lokasi', data='2'),
            PostbackAction(label='Foto/gambar', data='3'),
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

        #update email in database
        connection.rollback()
        postgres_update_query = """ UPDATE public.user_profile set email = %s where user_id = %s"""
        record_to_update = (msg, event.source.user_id)
        cursor.execute(postgres_update_query, record_to_update)
        connection.commit()  
    elif b == "0" and len(msg) > 7:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Anda belum memasukkan email, silahkan masukkan terlebih dahulu')) 
    elif msg.encode('unicode-escape').decode() in loc:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Terimakasih, data lokasi berhasil disimpan')) 
       
        #update loc in database
        connection.rollback()
        postgres_update_query = """ UPDATE public.complaint set loc = %s where user_id = %s and loc = %s"""
        record_to_update = (msg, event.source.user_id, "0")
        cursor.execute(postgres_update_query, record_to_update)
        connection.commit()    
    else :
        #text complaint
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Terimakasih atas waktunya, data berhasil disimpan\n id komplain : {}\n(simpan untuk update informasi komplain)'.format(event.message.id)))

        #search lokasi
        a = ["0"]
        for i in range(len(loc)):
            x = re.search(loc[i], msg)
            if x == None:
                pass
            else:
                a[0] = loc[i]
        location = a[0]

        #waktu komplain
        time = (datetime.fromtimestamp(event.timestamp/1e3).astimezone(tz= pytz.timezone('Asia/Jakarta'))).strftime("%m/%d/%Y, %H:%M:%S")

        #insert complaint data into database
        connection.rollback()
        postgres_insert_query = """ INSERT INTO public.complaint (message_id, user_id, teks, loc, "time") VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (event.message.id, event.source.user_id, msg, location, time)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        
#  Even saat user mengirim pesan gambar           
@handler.add(MessageEvent, message=(ImageMessage))
def handle_message_image(event):

    #email check
    connection.rollback()
    cursor.execute("SELECT * FROM public.user_profile WHERE user_id = %s", (event.source.user_id,))
    connection.commit()
    rows = cursor.fetchall()
    for row in rows:
        if row[2] == None:
            b = "0"
        else :
            b = "1"
    
### insert image message data into database
    #get image as binary 
    r = requests.get('https://api-data.line.me/v2/bot/message/{}/content'.format(event.message.id), headers={'Authorization' : 'Bearer DhLYkk/1uuQ130naHtlK2g7ebRDqe+OB0rVIGgFXqyRTf3zOCNTdEwYkDbDNOYF7MJNgHK1T21nK7s3Mvy+VboMpODA9uC5LzvqdqzjmtXZrR7+LnA4Wc9RK/rqeKJAbjSVSpz9qbanDOLFJdx6qxwdB04t89/1O/w1cDnyilFU='} )
    img = r.content

    #waktu
    time = (datetime.fromtimestamp(event.timestamp/1e3).astimezone(tz= pytz.timezone('Asia/Jakarta'))).strftime("%m/%d/%Y, %H:%M:%S")

    #insert image into database
    connection.rollback()
    postgres_insert_query = """ INSERT INTO public."Image" (id_image, user_id, "time", image) VALUES (%s,%s,%s,%s)"""
    record_to_insert = (event.message.id, event.source.user_id, time, img)
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()
###

###
    #image message date check from complaint table
    connection.rollback()
    cursor.execute("SELECT * FROM public.complaint WHERE user_id = %s", (event.source.user_id,))
    connection.commit()
    rows1 = cursor.fetchall()
    date1 = datetime.strptime(rows1[-1][4], "%m/%d/%Y, %H:%M:%S")

    #complaint message date check from Image table
    connection.rollback()
    cursor.execute("""SELECT * FROM public."Image" WHERE user_id = %s""", (event.source.user_id,))
    connection.commit()
    rows2 = cursor.fetchall()
    date2 = datetime.strptime(rows2[-1][2], "%m/%d/%Y, %H:%M:%S")

    #time differences
    delta = date2-date1
###

    if b == "0":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Anda belum memasukkan email, silahkan masukkan terlebih dahulu'))
    elif delta.seconds <= 60:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Terimakasih atas waktunya, gambar berhasil disimpan')) 
    elif delta.seconds > 60:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Apa ada keterangan fotonya?'))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Terimakasih atas waktunya, gambar berhasil disimpan')) 
 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
