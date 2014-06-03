import json
import pprint
from flask import Flask, render_template, request, abort, redirect
from flask_bootstrap import Bootstrap
from pony.orm import *
from db import db, Players

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/stats/<player>")
def player_view(player):
    player = Players.get(name=player)
    if player is None:
        abort(404)
    stats = {
        "Captures": player.captures,
        "Disconnects": player.disconnects,
        "Drops": player.drops,
        "Games": player.games,
        "Grabs": player.grabs,
        "Hold": player.hold,
        "Hours": player.hours,
        "Losses": player.losses,
        "Popped": player.popped,
        "Prevent": player.prevent,
        "Returns": player.returns,
        "Support": player.support,
        "Tags": player.tags,
        "Wins": player.wins}
    return render_template('stats.html', name=player.name, stats=stats)

@app.route("/stats", methods=["GET"])
def stat_redirect():
    name = request.args.get('player_name')
    return redirect("/stats/"+name)

@app.route("/autocomplete")
def autocomplete():
    name = request.args.get('term')
    if name is None:
        return json.dumps([])
    d = json.dumps(list(select(c.name for c in Players if c.name.lower().startswith(name.lower()) and len(c.name) > 0).order_by(lambda k: k.lower())[:50]))
    return d
if __name__ == "__main__":
    app.wsgi_app = with_transaction(app.wsgi_app)
    app.run(debug=True)
