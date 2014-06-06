import json
import pprint
from flask import Flask, render_template, request, abort, redirect
from flask_bootstrap import Bootstrap
import inflection
from pony.orm import *
from db import db, Player, WeeklyStats, MonthlyStats, DailyStats
import humanize
app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def index():
    return render_template('index.html')
#sql_debug(True)

@app.route("/radar/<player>")
def radar_view(player):
    player = Player.get(name=player)
    if player is None:
        abort(404)

    max_caps = (max(p.captures_per_game for p in Player if p.games > 250))
    max_drops = (max(p.drops_per_game for p in Player if p.games > 250))
    max_hold = (max(p.hold_per_game for p in Player if p.games > 250))
    max_popped = (max(p.popped_per_game for p in Player if p.games > 250))
    max_prevent = (max(p.prevent_per_game for p in Player if p.games > 250))
    max_returns = (max(p.returns_per_game for p in Player if p.games > 250))
    max_support = (max(p.support_per_game for p in Player if p.games > 250))
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
    player = Player.get(name=player)
    if player is None:
        abort(404)
    keys = ["Captures", "Disconnects", "Drops", "Games", "Grabs", "Hold", "Hours",
     "Losses", "Popped", "Prevent", "Returns", "Support", "Tags", "Wins"]
    stats = {
        "Captures": player.all_time.captures,
        "Disconnects": player.all_time.disconnects,
        "Drops": player.all_time.drops,
        "Games": player.all_time.games,
        "Grabs": player.all_time.grabs,
        "Hold": player.all_time.hold,
        "Hours": player.all_time.hours/60/60,
        "Losses": player.all_time.losses,
        "Popped": player.all_time.popped,
        "Prevent": player.all_time.prevent,
        "Returns": player.all_time.returns,
        "Support": player.all_time.support,
        "Tags": player.all_time.tags,
        "Wins": player.all_time.wins}
    monthly = select(x for x in MonthlyStats).order_by(lambda x: desc(x.period)).limit(1)[0]
    monthly_stats = dict(zip(keys, (monthly.captures, monthly.disconnects, monthly.drops,
                                    monthly.games, monthly.grabs, monthly.hold,
                                    monthly.hours/60/60, monthly.losses, monthly.popped,
                                    monthly.prevent, monthly.returns, monthly.support,
                                    monthly.tags, monthly.wins)))
    weekly = select(x for x in WeeklyStats).order_by(lambda x: desc(x.period)).limit(1)[0]
    weekly_stats = dict(zip(keys, (weekly.captures, weekly.disconnects, weekly.drops,
                                    weekly.games, weekly.grabs, weekly.hold,
                                    weekly.hours/60/60, weekly.losses, weekly.popped,
                                    weekly.prevent, weekly.returns, weekly.support,
                                    weekly.tags, weekly.wins)))
    daily = select(x for x in DailyStats).order_by(lambda x: desc(x.period)).limit(1)[0]
    daily_stats = dict(zip(keys, (daily.captures, daily.disconnects, daily.drops,
                                daily.games, daily.grabs, daily.hold,
                                daily.hours/60/60, daily.losses, daily.popped,
                                daily.prevent, daily.returns, daily.support,
                                daily.tags, daily.wins)))
    ranks = {k: 0 for k in stats.keys()}#getattr(player.all_time.ranks, k.lower(), 'Unknown') for k in stats.keys()}
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
    d = json.dumps(select(c.name for c in Player if c.name.lower().startswith(name.lower()) and len(c.name) > 0).order_by(lambda k: k.lower())[:50])
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
