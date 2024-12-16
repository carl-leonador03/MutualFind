import requests
from base64 import b64decode as b64d, b64encode as b64e

from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for

import os
import bot
import asyncio, threading

API_ENDPOINT = "https://discord.com/api/v10"
CLIENT_ID = "1293198029654065182"
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = "https://mutualfind.koyeb.app/authorize"

app = Flask(__name__)

def exchange_code(code):
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data = data, headers = headers, auth = (CLIENT_ID, CLIENT_SECRET))
    return r.json()

def refresh_token(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.post("%s/oauth2/token" % API_ENDPOINT, data = data, headers = headers, auth = (CLIENT_ID, CLIENT_SECRET))
    return r.json()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/authorize")
def auth():
    if "code" not in request.args.keys():
        scopes = [
            'guilds',
            'guilds.members.read',
            'identify'
        ]

        auth_url = "https://discord.com/oauth2/authorize"

        return redirect(f"{auth_url}?client_id={CLIENT_ID}&response_type=code&redirect_uri={requests.utils.quote(REDIRECT_URI)}&scope={'+'.join(scopes)}")
    
    elif "code" in request.args.keys():
        code = request.args['code']
        res_json = exchange_code(code)

        return make_response("""<script type="javascript/json">function done() { try { window.opener.getCode(\"""" + str(b64e(str(res_json).encode())) + """\") } catch (err) {} window.close(); return false; } </script><body onload="done();">Authorized</body>""", 200)
    
    else:
        return make_response("Forbidden", 403)

@app.route("/fetch", methods=["POST"])
def fetch():
    if request.method == "POST":
        if "guild_id" in request.args:

            task = asyncio.run_coroutine_threadsafe(bot.get_members(request.args["guild_id"]), loop)
            result = task.result()

            return jsonify(result)
        else:
            return jsonify({"Missing argument": "guild_id not given."})
    
    else:
        return jsonify({"Forbidden": 403})

def bot_loop_start(loop):
    loop.run_forever()

def bot_start(loop):
    loop.create_task(bot.start_bot())
    bot_thread = threading.Thread(target = bot_loop_start, args=(loop,))
    bot_thread.start()

loop = asyncio.get_event_loop()
bot_start(loop)
app.run()