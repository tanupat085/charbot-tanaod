from flask import Flask, json, jsonify, render_template ,request ,make_response

import geopy.distance as ps
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("product").sheet1
data = sheet.get_all_records()
listdata = pd.DataFrame(data)
print(listdata)

app = Flask(__name__)


def create_flex(name):
    flex_json = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "image",
                    "url": "https://pbs.twimg.com/profile_images/1305645851491135489/UeURmV3s.jpg",
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "150:196",
                    "gravity": "center",
                    "flex": 1
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "NEW",
                        "size": "xs",
                        "color": "#ffffff",
                        "align": "center",
                        "gravity": "center"
                    }
                    ],
                    "backgroundColor": "#EC3D44",
                    "paddingAll": "2px",
                    "paddingStart": "4px",
                    "paddingEnd": "4px",
                    "flex": 0,
                    "position": "absolute",
                    "offsetStart": "18px",
                    "offsetTop": "18px",
                    "cornerRadius": "100px",
                    "width": "48px",
                    "height": "25px"
                }
                ]
            }
            ],
            "paddingAll": "0px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "contents": [],
                        "size": "xl",
                        "wrap": True,
                        "text": name ,
                        "color": "#ffffff",
                        "weight": "bold"
                    }
                    ],
                    "spacing": "sm"
                }
                ]
            }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#464F69"
        }
    }
    return [{
        "type": "flex",
        "altText": "Show Carousel",
        "contents": {
            "type": "carousel",
            "contents": [
                flex_json,
                flex_json
            ]
        }
    }]

@app.route("/")
def home():
    return render_template('index.html')
#! การสร้าง Html หน้า Web จะต้องสร้าง Folder ชื่อ Templates มาเก็บ HTML

@app.route("/get_profile")
def get_profile():
    name = "test tanup"
    jsonData = create_flex(name)
    #return jsonify(jsonData) #? สำหรับ API แบบที่ 1
    #? เป็นการเรียก Line Payload
    response= make_response(
                jsonify({"line_payload": jsonData}),200,
    )
    response.headers["Response-Type"] = "object"
    return response  #? สำหรับ API แบบที่ 2 

@app.route("/insert_order")
def insert_order():
    name = request.args.get("name")
    stock = request.args.get("stock")
    order = request.args.get("order")
    add_data = [name, str(stock),str(order)]
    data = sheet.get_all_records()
    listdata = pd.DataFrame(data)
    index = int(len(listdata) + 2)
    sheet.insert_row(add_data , index)
    return "ok"

@app.route("/get_order")
def get_order():
    name = request.args.get("name")
    data = sheet.get_all_records()
    listdata = pd.DataFrame(data)
    data = listdata[listdata['ชื่อ'] == name ]
    if len(data) == 0 :
        return "no data"
    jsonData = {
        "name":data.iloc[0]['ชื่อ'],
        "stock":str(data.iloc[0]['จำนวนสินค้า']),
        "order":str(data.iloc[0]['จำนวนสั่ง'])
    }
    return jsonify(jsonData)

if __name__ == "__main__":
    app.run(port=5000,debug=True)