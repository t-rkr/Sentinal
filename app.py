from flask import Flask,jsonify, render_template, redirect, request, url_for
import requests


app = Flask(__name__)


@app.route('/chatbot')
def chatbot():
    return render_template('tabs/chatbot.html')

@app.route('/chat',methods=["POST"])
def chat():
    message = request.form['message']
    querystring = {"message": message}
    reply = requests.request("POST",app.config["CHAT"],params=querystring).json()
    return reply


@app.route('/timeline')
def timeline():
    querystring_d = {"scope": "day"}
    querystring_m = {"scope": "month"}
    metrics_day = requests.request("GET", app.config["METRICS"], params=querystring_d).json()
    metrics_month = requests.request("GET", app.config["METRICS"], params=querystring_m).json()

    return render_template('tabs/timeline.html')

@app.route('/tweets')
def tweets():
    t_data = requests.get(app.config["TWEETS_DATA"]).json()
    return render_template('tabs/tweets.html',t_data=t_data)

@app.route('/')
def index():
    try:
        #timeline graph
        metrics_d = requests.get(app.config["METRICS"],params={"scope": "day"}).json()
        metrics_m = requests.get(app.config["METRICS"],params={"scope": "month"}).json()

        #Most recent tweets
        t_data = requests.get(app.config["TWEETS"]).json()

        #Sentiment data
        s_data = requests.get(app.config["POLARITY"]).json()

        #Unique users
        user_metrics = requests.get(app.config["USER_METRICS"],params={"scope":"day"}).json()
        user__monthly_metrics = requests.get(app.config["USER_METRICS"],params={"scope":"month"}).json()

        #greviences
        g_data = requests.get(app.config["GREV"]).json()

        #Total data
        total_tweets = requests.get(app.config["TOTAL_TWEETS"]).json()


        return render_template('index.html',t_data=t_data, s_data=s_data,metrics_d=metrics_d,metrics_m=metrics_m,
                               user_metrics=user_metrics,total_tweets=total_tweets,
                               user__monthly_metrics=user__monthly_metrics,g_data=g_data)
    except Exception as m:
        print(m)
        return render_template('errors/500.html')


if __name__ == '__main__':
    app.config.update(
        TWEETS_DATA="http://127.0.0.1:5000/tweetsData",
        TOTAL_TWEETS="http://127.0.0.1:5000/totalTweets",
        GREV = "http://127.0.0.1:5000/grev",
        USER_METRICS = "http://127.0.0.1:5000/userMetrics",
        POLARITY = "http://127.0.0.1:5000/polarity",
        TWEETS = "http://127.0.0.1:5000/tweets",
        METRICS = "http://127.0.0.1:5000/metrics",
        CHAT = "http://127.0.0.1:5000/chat"
    )
    app.run(port=9001)
