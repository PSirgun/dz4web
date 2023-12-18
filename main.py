from flask import Flask, render_template, request, send_file
import socket
import json
from datetime import datetime
import threading
from pathlib import Path

host = '127.0.0.1'
port_http = 3000 
port_socket = 5000

app = Flask(__name__, static_url_path='/static')

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/message.html', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form['username']
        message_text = request.form['message']

        socket_client(username, message_text)

    return render_template('message.html')

@app.errorhandler(Exception)
def error(_):
    return render_template('error.html'), 404

@app.route('/logo.png') 
def get_logo():
    logo_path = 'static/logo.png'
    return send_file(logo_path, mimetype='image/png')


@app.route('/style.css')  
def get_style():
    style_path = 'static/style.css'
    return send_file(style_path, mimetype='text/css')

def socket_server():

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port_socket))

        print ('\n\nSucsess conection - socket\n\n')

        while True:
                data, addr = server.recvfrom(1024)
                data_dict = json.loads(data.decode('utf-8'))
                save_to_json(data_dict)


def socket_client(username, message_text):
   
    now_time = str(datetime.now())
    
    data_dict = {
        now_time: {
            "username": username,
            "message": message_text
        }
    }

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.sendto(json.dumps(data_dict).encode('utf-8'), (host, port_socket))

def save_to_json(data_dict):

    with open('storage/data.json', 'a') as f:
        json.dump(data_dict, f)
        f.write('\n')
        print ("ok")

if __name__ == '__main__':
    socket_thread = threading.Thread(target=socket_server) 
    http_thread = threading.Thread(target=app.run, kwargs={'port': port_http}) 
    http_thread.start()
    socket_thread.start()