import json
import pprint
from flask import Flask, render_template, request, abort, redirect
from flask_bootstrap import Bootstrap
import inflection
from pony.orm import *
from db import db, Players
import humanize
app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def index():
    return render_template('index.html')
#sql_debug(True)

@app.route("/radar/<player>")
def radar_view(player):
    player = Players.get(name=player)
    if player is None:
        abort(404)

    max_caps = (max(p.captures_per_game for p in Players if p.games > 250))
    max_drops = (max(p.drops_per_game for p in Players if p.games > 250))
    max_hold = (max(p.hold_per_game for p in Players if p.games > 250))
    max_popped = (max(p.popped_per_game for p in Players if p.games > 250))
    max_prevent = (max(p.prevent_per_game for p in Players if p.games > 250))
    max_returns = (max(p.returns_per_game for p in Players if p.games > 250))
    max_support = (max(p.support_per_game for p in Players if p.games > 250))
    print max_caps

    caps = player.captures_per_game/max_caps
    drops = player.drops_per_game/max_drops
    hold = player.hold_per_game/max_hold
    popped = player.popped_per_game/max_popped
    prevent = player.prevent_per_game/max_prevent
    returns = player.returns_per_game/max_returns
    support = player.support_per_game/max_support
    return json.dumps([caps, drops, hold, popped, prevent, returns, support])

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
        "Hours": player.hours/60/60,
        "Losses": player.losses,
        "Popped": player.popped,
        "Prevent": player.prevent,
        "Returns": player.returns,
        "Support": player.support,
        "Tags": player.tags,
        "Wins": player.wins}
    ranks = {k: getattr(player.ranks, k.lower(), 'Unknown') for k in stats.keys()}
    return render_template('stats.html', name=player.name, stats=stats, ranks=ranks, profile_string=player.profile_string, last_updated=player.last_updated)

@app.route("/stats", methods=["GET"])
def stat_redirect():
    name = request.args.get('player_name')
    return redirect("/stats/"+name)

@app.route("/autocomplete")
def autocomplete():
    name = request.args.get('term')
    if name is None:
        return json.dumps([])
    d = json.dumps(select(c.name for c in Players if c.name.lower().startswith(name.lower()) and len(c.name) > 0).order_by(lambda k: k.lower())[:50])
    return d

@app.route("/top")
def top():
    return "TODO"

@app.route("/help")
def help():
    return "TODO"

@app.route("/compare")
def compare():
    return "TODO"

@app.route("/about")
def about():
    return "TODO"

if __name__ == "__main__":
    app.wsgi_app = with_transaction(app.wsgi_app)
    app.jinja_env.globals.update(ordinalize=inflection.ordinalize)
    app.jinja_env.globals.update(humanize=humanize.naturaltime)
    app.run(debug=True)
