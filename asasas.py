import requests
import psycopg2
import pandas

connection = psycopg2.connect(user="uigronqdtlgfgy",
                              password="a35b4e9e8ed6798ee17180222a67fd77fe9109fac5163cefd5b20ac405894e96",
                              host="ec2-52-207-25-133.compute-1.amazonaws.com",
                              port="5432",
                              database="d9npil276i06um")
cursor = connection.cursor()

r = requests.get('https://api-data.line.me/v2/bot/message/{}/content'.format('12371467712925'), headers={'Authorization' : 'Bearer DhLYkk/1uuQ130naHtlK2g7ebRDqe+OB0rVIGgFXqyRTf3zOCNTdEwYkDbDNOYF7MJNgHK1T21nK7s3Mvy+VboMpODA9uC5LzvqdqzjmtXZrR7+LnA4Wc9RK/rqeKJAbjSVSpz9qbanDOLFJdx6qxwdB04t89/1O/w1cDnyilFU='} )
img  = r.content


postgres_insert_query = """ INSERT INTO public."Gambar" (id_gambar, user_id, waktu, gambar) VALUES (%s,%s,%s,%s)"""
record_to_insert = (int('1253637181763'),'Uf4cd52ad9107eaadce5392f5fe5635e8', '07/23/2020, 22:23:55', img)
cursor.execute(postgres_insert_query, record_to_insert)
connection.commit()