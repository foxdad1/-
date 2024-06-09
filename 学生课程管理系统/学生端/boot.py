import flask
import pymysql
import requests
import json
from flask import request, jsonify, session, redirect, url_for, render_template

app = flask.Flask(__name__)

db = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='student', charset='utf8')
cursor = db.cursor()
users = []


@app.route("/", methods=["GET", "POST"])
def login():
    session['login'] = ''
    msg = ''
    if request.method == 'POST':
        user = request.form.get("user", "")
        pwd = request.form.get("pwd", "")
        sql1 = "SELECT * FROM sys_user WHERE username=%s AND password=%s;"
        cursor.execute(sql1, (user, pwd))
        result = cursor.fetchone()
        if result:
            session['login'] = 'OK'
            users.append(user)
            return redirect(url_for('index'))
        else:
            msg = '用户名或密码错误'
    return render_template('login.html', msg=msg)


@app.route("/index", methods=["GET"])
def index():
    if session.get("login", "") == '':
        return redirect('/')
    user_info = users[-1] if users else ''
    sql_list = "SELECT * FROM students_infos"
    cursor.execute(sql_list)
    results = cursor.fetchall()
    return render_template('index.html', user_info=user_info, results=results)


# 调用文心一言API
API_KEY = "8F7b49MQtWW2bCqig9HDG77O"
SECRET_KEY = "R3deIlQ9xoAmdkqKiVwBVo2V0T4oNaC1"


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    response = requests.post(url, params=params)
    return response.json().get("access_token")


def get_response(message):
    access_token = get_access_token()
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"
    payload = json.dumps({"messages": [{"role": "user", "content": message}]})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)

    # 打印整个响应数据以调试
    print(response.json())

    response_data = response.json()

    # 确认响应数据结构并提取 result 字段
    if 'result' in response_data:
        return response_data['result']
    else:
        return "今日调用次数已达上限"


@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Invalid message"}), 400
    try:
        ai_reply = get_response(user_message)
        user = users[-1] if users else 'unknown'
        sql_insert = "INSERT INTO ai_chat (user, user_message, ai_reply) VALUES (%s, %s, %s)"
        cursor.execute(sql_insert, (user, user_message, ai_reply))
        db.commit()
        return jsonify({"reply": ai_reply})
    except Exception as e:
        print(e)
        return jsonify({"error": "Error communicating with Wenxin Yiyan API"}), 500


@app.route("/get_chat_history", methods=["GET"])
def get_chat_history():
    username = request.args.get('username')
    if username:
        sql_select = "SELECT user_message, ai_reply, timestamp FROM ai_chat WHERE user = %s ORDER BY timestamp ASC"
        cursor.execute(sql_select, (username,))
        results = cursor.fetchall()

        chat_history = []
        for result in results:
            chat_history.append(
                {'sender': 'user', 'message': result[0], 'timestamp': result[2]})
            chat_history.append(
                {'sender': 'ai', 'message': result[1], 'timestamp': result[2]})

        return jsonify({'messages': chat_history})
    else:
        return jsonify({'error': '未提供用户名'}), 400

@app.route("/delete_message", methods=["POST"])
def delete_message():
    data = request.json
    username = data.get('username')
    index = data.get('index')
    if username is not None and index is not None:
        sql_select = "SELECT id FROM ai_chat WHERE user = %s ORDER BY timestamp ASC"
        cursor.execute(sql_select, (username,))
        results = cursor.fetchall()
        if 0 <= index < len(results) // 2:
            message_id = results[index * 2][0]  # 每个用户消息后面是AI回复，乘2获取用户消息的ID
            sql_delete = "DELETE FROM ai_chat WHERE id = %s"
            cursor.execute(sql_delete, (message_id,))
            db.commit()
            return jsonify({"success": '成功删除'})
        else:
            return jsonify({"error": "删除失败"}), 400
    else:
        return jsonify({"error": "数据不存在！"}), 400


app.debug = True
app.secret_key = 'carson'
try:
    app.run()
except Exception as err:
    print(err)
    db.close()
