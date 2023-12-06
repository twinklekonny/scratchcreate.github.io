from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# 初期のデータベース
data_list = [
    {'fiveDigit': [34567], 'twoDigit': [3]},
    {'fiveDigit': [12345], 'twoDigit': [1]}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.json
    input_five_digit = data.get('fiveDigit', [])
    input_two_digit = data.get('twoDigit', [])

    # 入力された数字をデータベースと照合
    for item in data_list:
        if input_five_digit == item['fiveDigit'] and input_two_digit == item['twoDigit']:
            return jsonify({"message": "Correct password!"}), 200  # パスワードが正しければJSONレスポンスを返す

        # パスワードがリスト内の要素として一致するかを確認
        if input_five_digit[0] in item['fiveDigit'] and input_two_digit[0] in item['twoDigit']:
            return jsonify({"message": "Correct password!"}), 200  # パスワードが正しければJSONレスポンスを返す

    # パスワードが正しくない場合の処理
    return jsonify({"message": "Incorrect password."}), 401

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    socketio.emit('message', message)

if __name__ == '__main__':
    socketio.run(app)





