import json
import pprint
from flask import Flask, render_template, request, abort, redirect
from flask_bootstrap import Bootstrap
import inflection
from pony.orm import *
from db import Session, AllTimeStats, MonthlyStats, WeeklyStats, DailyStats, Player
import humanize
app = Flask(__name__)
Bootstrap(app)
session = Session()

@app.route("/")
def index():
    return render_template('index.html')
#sql_debug(True)

@app.route("/radar/<player>")
def radar_view(player):
    player = session.query(Player).filter_by(name=player).first()
    stats = player.all_time_stats
    c = session.query(AllTimeStats)
    max_caps = c.order_by(
        AllTimeStats.captures_per_game.desc()).filter(AllTimeStats.captures_per_game is not None).first()
    max_drops = c.order_by(
        AllTimeStats.drops_per_game.desc()).first().drops_per_game
    max_hold = c.order_by(
        AllTimeStats.hold_per_game.desc()).first().hold_per_game
    max_popped = c.order_by(
        AllTimeStats.popped_per_game.desc()).first().popped_per_game
    max_prevent = c.order_by(
        AllTimeStats.prevent_per_game.desc()).first().prevent_per_game
    max_returns = c.order_by(
        AllTimeStats.returns_per_game.desc()).first().returns_per_game
    max_support = c.order_by(
        AllTimeStats.support_per_game.desc()).first().support_per_game

    caps = stats.captures_per_game/max_caps
    drops = stats.drops_per_game/max_drops
    hold = stats.hold_per_game/max_hold
    popped = stats.popped_per_game/max_popped
    prevent = stats.prevent_per_game/max_prevent
    returns = stats.returns_per_game/max_returns
    support = stats.support_per_game/max_support
    return json.dumps([caps, drops, hold, popped, prevent, returns, support])

@app.route("/stats/<player>")
def player_view(player):
    player = session.query(Player).filter_by(name=player).first()
    if player is None:
        abort(404)
    keys = ["Captures", "Disconnects", "Drops", "Games", "Grabs", "Hold", "Hours",
     "Losses", "Popped", "Prevent", "Returns", "Support", "Tags", "Wins"]
    stats = {
        "Captures": player.all_time_stats.captures,
        "Disconnects": player.all_time_stats.disconnects,
        "Drops": player.all_time_stats.drops,
        "Games": player.all_time_stats.games,
        "Grabs": player.all_time_stats.grabs,
        "Hold": player.all_time_stats.hold,
        "Hours": player.all_time_stats.hours/60/60,
        "Losses": player.all_time_stats.losses,
        "Popped": player.all_time_stats.popped,
        "Prevent": player.all_time_stats.prevent,
        "Returns": player.all_time_stats.returns,
        "Support": player.all_time_stats.support,
        "Tags": player.all_time_stats.tags,
        "Wins": player.all_time_stats.wins}
    monthly = session.query(MonthlyStats).current().filter_by(player=player.profile_string).first()
    monthly_stats = dict(zip(keys, (monthly.captures, monthly.disconnects, monthly.drops,
                                    monthly.games, monthly.grabs, monthly.hold,
                                    monthly.hours/60/60, monthly.losses, monthly.popped,
                                    monthly.prevent, monthly.returns, monthly.support,
                                    monthly.tags, monthly.wins)))
    weekly = session.query(WeeklyStats).current().filter_by(
        player=player.profile_string).first()
    weekly_stats = dict(zip(keys, (weekly.captures, weekly.disconnects, weekly.drops,
                                    weekly.games, weekly.grabs, weekly.hold,
                                    weekly.hours/60/60, weekly.losses, weekly.popped,
                                    weekly.prevent, weekly.returns, weekly.support,
                                    weekly.tags, weekly.wins)))
    daily = session.query(DailyStats).current().filter_by(
        player=player.profile_string).first()
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
    names = session.query(Player.name).filter(Player.name.like('{}%'.format(name))).limit(50).all()
    d = json.dumps([x[0] for x in names])
    print d
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
