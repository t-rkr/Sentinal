from flask import Flask,jsonify, render_template, redirect, request, url_for
import requests


app = Flask(__name__)


@app.route('/chatbot')
def chatbot():
    return render_template('tabs/chatbot.html')

@app.route('/chat',methods=["POST"])
def chat():
    message = request.form['message']
    print(message)
    url = "http://127.0.0.1:5000/chat"
    querystring = {"message": message}
    reply = requests.request("POST",url,params=querystring).json()
    return reply

@app.route('/metrics')
def get_metrics():
    url = "http://127.0.0.1:5000/metrics"

    querystring_d = {"scope": "day"}
    querystring_m = {"scope": "month"}

    metrics_day = requests.request("GET", url, params=querystring_d).json()
    metrics_month = requests.request("GET", url, params=querystring_m).json()

    return 0

@app.route('/timeline')
def timeline():
    url = "http://127.0.0.1:5000/metrics"
    querystring_d = {"scope": "day"}
    querystring_m = {"scope": "month"}
    metrics_day = requests.request("GET", url, params=querystring_d).json()
    metrics_month = requests.request("GET", url, params=querystring_m).json()

    metrics_day_k = list(metrics_day.keys())
    metrics_day_v = list(metrics_day.values())
    metrics_month_k = [str(x) for x in list(metrics_month.keys())]
    metrics_month_v = list(metrics_month.values())



    return render_template('tabs/timeline.html',metrics_day_k=metrics_day_k,
                                                                   metrics_day_v=metrics_day_v,
                           metrics_month_k=metrics_month_k,metrics_month_v=metrics_month_v)

@app.route('/tweets')
def tweets():
    t_data = requests.get("http://127.0.0.1:5000/tweetsData").json()
    return render_template('tabs/tweets.html',t_data=t_data)

@app.route('/')
def index():
    try:
        #timeline graph
        metrics_d = requests.get("http://127.0.0.1:5000/metrics",params={"scope": "day"}).json()
        metrics_m = requests.get("http://127.0.0.1:5000/metrics",params={"scope": "month"}).json()
        metrics_day_k = list(metrics_d.keys())
        metrics_day_v = list(metrics_d.values())
        metrics_month_k = list(metrics_m.keys())
        metrics_month_v = list(metrics_m.values())


        #Most recent tweets
        t_data = requests.get("http://127.0.0.1:5000/tweets").json()

        #Sentiment data
        s_data = requests.get("http://127.0.0.1:5000/polarity").json()

        #Unique users
        user_metrics = requests.get("http://127.0.0.1:5000/userMetrics",params={"scope":"day"}).json()
        user__monthly_metrics = requests.get("http://127.0.0.1:5000/userMetrics",params={"scope":"month"}).json()

        #greviences
        g_data = requests.get("http://127.0.0.1:5000/grev").json()


        total_tweets = requests.get("http://127.0.0.1:5000/totalTweets").json()


        return render_template('index.html',t_data=t_data, s_data=s_data,metrics_day_k=metrics_day_k,
                                                                       metrics_day_v=metrics_day_v,
                               metrics_month_k=metrics_month_k,metrics_month_v=metrics_month_v,
                               user_metrics=user_metrics,total_tweets=total_tweets,
                               user__monthly_metrics=user__monthly_metrics,g_data=g_data)
    except Exception as m:
        print(m)
        return render_template('errors/500.html')

#
# @app.route('/send_message', methods=['POST'])
# def chatbot_message():
#     message = str(request.get_data(),'utf-8').split("=")[1]
#     chat_response = chatbot.chatbot_response(message)
#     return "Okay cool"
#

if __name__ == '__main__':
    app.run(port=9001)
