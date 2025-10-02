from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session
import psycopg2
# import os
from os import environ as env
from authlib.integrations.flask_client import OAuth
import json
from urllib.parse import quote_plus, urlencode
# from dotenv import load_dotenv

# load_dotenv()


app = Flask(__name__)
app.secret_key = env["FLASK_SECRET"]

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)



# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    # this is where you would check username and password in database
    session["user"] = token
    return redirect("/")



# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("hello", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )
    

@app.route('/')
def hello(name=None):
    return render_template("hello.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/submit-guestbook', methods=['POST'])
def submit_guestbook():
    name = request.form['name']
    message = request.form['message']
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    insert_sql = 'INSERT INTO guestbook (name, message) VALUES (%s, %s);'
    cursor.execute(insert_sql, (name, message))
    conn.commit()
    
    cursor.close()
    conn.close()
    return render_template('guestbook.html')

