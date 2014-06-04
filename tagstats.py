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
    keys = ["Captures", "Disconnects", "Drops", "Games", "Grabs", "Hold", "Hours",
     "Losses", "Popped", "Prevent", "Returns", "Support", "Tags", "Wins"]
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
    monthly_stats = dict(zip(keys, (player.monthly.captures, player.monthly.disconnects, player.monthly.drops,
                                    player.monthly.games, player.monthly.grabs, player.monthly.hold,
                                    player.monthly.hours/60/60, player.monthly.losses, player.monthly.popped,
                                    player.monthly.prevent, player.monthly.returns, player.monthly.support,
                                    player.monthly.tags, player.monthly.wins)))
    weekly_stats = dict(zip(keys, (player.weekly.captures, player.weekly.disconnects, player.weekly.drops,
                                    player.weekly.games, player.weekly.grabs, player.weekly.hold,
                                    player.weekly.hours/60/60, player.weekly.losses, player.weekly.popped,
                                    player.weekly.prevent, player.weekly.returns, player.weekly.support,
                                    player.weekly.tags, player.weekly.wins)))
    daily_stats = dict(zip(keys, (player.daily.captures, player.daily.disconnects, player.daily.drops,
                                player.daily.games, player.daily.grabs, player.daily.hold,
                                player.daily.hours/60/60, player.daily.losses, player.daily.popped,
                                player.daily.prevent, player.daily.returns, player.daily.support,
                                player.daily.tags, player.daily.wins)))
    ranks = {k: getattr(player.ranks, k.lower(), 'Unknown') for k in stats.keys()}
    return render_template('stats.html', name=player.name, stats=stats, ranks=ranks, profile_string=player.profile_string, last_updated=player.last_updated,
                           monthly_stats=monthly_stats, weekly_stats=weekly_stats, daily_stats=daily_stats)

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
    app.jinja_env.globals.update(sorted=sorted)
    app.jinja_env.globals.update(iter=iter)
    app.run(debug=True)
