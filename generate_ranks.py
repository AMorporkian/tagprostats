from db import *

"""
    captures = Optional(int)
    disconnects = Optional(int)
    drops = Optional(int)
    games = Optional(int)
    grabs = Optional(int)
    hold = Optional(int)
    hours = Optional(int)
    losses = Optional(int)
    non_return_tags = Optional(int)
    popped = Optional(int)
    prevent = Optional(int)
    returns = Optional(int)
    support = Optional(int)
    tags = Optional(int)
"""
# sql_debug(True)
with db_session:
    data = dict(captures=select(p for p in Players).order_by(
        lambda p: desc(p.captures)),
                disconnects=select(p for p in Players).order_by(
                    lambda p: desc(p.disconnects)),
                drops=select(p for p in Players).order_by(
                    lambda p: desc(p.drops)),
                games=select(p for p in Players).order_by(
                    lambda p: desc(p.games)),
                grabs=select(p for p in Players).order_by(
                    lambda p: desc(p.grabs)),
                hold=select(p for p in Players).order_by(
                    lambda p: desc(p.hold)),
                hours=select(p for p in Players).order_by(
                    lambda p: desc(p.hours)),
                losses=select(p for p in Players).order_by(
                    lambda p: desc(p.losses)),
                popped=select(p for p in Players).order_by(
                    lambda p: desc(p.popped)),
                prevent=select(p for p in Players).order_by(
                    lambda p: desc(p.prevent)),
                returns=select(p for p in Players).order_by(
                    lambda p: desc(p.returns)),
                support=select(p for p in Players).order_by(
                    lambda p: desc(p.support)),
                tags=select(p for p in Players).order_by(
                    lambda p: desc(p.tags)),
                wins=select(p for p in Players).order_by(
                    lambda p: desc(p.wins)))


    for k, v in data.iteritems():
        print k
        for i, player in enumerate(v):
            setattr(player.ranks, k, i)
    commit()