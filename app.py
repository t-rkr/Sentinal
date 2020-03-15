from flask import Flask,jsonify, render_template, redirect, request, url_for


app = Flask(__name__)


@app.route('/chatbot')
def chatbot():
    return render_template('tabs/chatbot.html')

@app.route('/timeline')
def timeline():
    return render_template('tabs/timeline.html')

@app.route('/tweets')
def tweets():
    return render_template('tabs/tweets.html')

@app.route('/')
def hello_world():
    return render_template('index.html')
#
# @app.route('/send_message', methods=['POST'])
# def chatbot_message():
#     message = str(request.get_data(),'utf-8').split("=")[1]
#     chat_response = chatbot.chatbot_response(message)
#     return "Okay cool"
#

if __name__ == '__main__':
    app.run(port=9001)
