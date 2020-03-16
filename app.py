from flask import Flask,jsonify, render_template, redirect, request, url_for
import requests


app = Flask(__name__)


@app.route('/chatbot')
def chatbot():
    return render_template('tabs/chatbot.html')

@app.route('/timeline')
def timeline():
    url = "http://127.0.0.1:5000/metrics"

    querystring_d = {"scope": "day"}
    querystring_m = {"scope": "month"}

    metrics_day = requests.request("GET", url, params=querystring_d).json()
    metrics_month = requests.request("GET", url, params=querystring_m).json()

    return render_template('tabs/timeline.html',metrics_day_k=[str(x) for x in list(metrics_day.keys())],
                                                                   metrics_day_v=list(metrics_day.values()),
                           metrics_month_k=[str(x) for x in list(metrics_month.keys())],metrics_month_v=list(
            metrics_month.values()))

@app.route('/tweets')
def tweets():
    return render_template('tabs/tweets.html')

@app.route('/')
def hello_world():

    #Most recent tweets
    t_data = requests.get("http://127.0.0.1:5000/tweets").json()

    #Sentiment data
    s_data = requests.get("http://127.0.0.1:5000/polarity").json()

    return render_template('index.html',t_data=t_data, s_data=s_data)
#
# @app.route('/send_message', methods=['POST'])
# def chatbot_message():
#     message = str(request.get_data(),'utf-8').split("=")[1]
#     chat_response = chatbot.chatbot_response(message)
#     return "Okay cool"
#

if __name__ == '__main__':
    app.run(port=9001)
