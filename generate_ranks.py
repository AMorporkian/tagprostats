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
rankable_stats = ['captures', 'disconnects', 'drops', 'games', 'grabs',
                  'hold', 'hours', 'losses', 'non_return_tags', 'popped',
                  'prevent', 'returns', 'support', 'tags']
sql_debug(True)
with db_session:
    data = dict(
    captures = [x.name for x in select(p for p in Players).order_by(lambda p: p.captures)],
    disconnects = [x.name for x in select(p for p in Players).order_by(lambda p: p.disconnects)],
    drops = [x.name for x in select(p for p in Players).order_by(lambda p: p.drops)],
    games = [x.name for x in select(p for p in Players).order_by(lambda p: p.games)],
    grabs = [x.name for x in select(p for p in Players).order_by(lambda p: p.grabs)],
    hold = [x.name for x in select(p for p in Players).order_by(lambda p: p.hold)],
    hours = [x.name for x in select(p for p in Players).order_by(lambda p: p.hours)],
    losses = [x.name for x in select(p for p in Players).order_by(lambda p: p.losses)],
    non_return_tags = [x.name for x in select(p for p in Players).order_by(lambda p: p.non_return_tags)],
    popped = [x.name for x in select(p for p in Players).order_by(lambda p: p.popped)],
    prevent = [x.name for x in select(p for p in Players).order_by(lambda p: p.prevent)],
    returns = [x.name for x in select(p for p in Players).order_by(lambda p: p.returns)],
    support = [x.name for x in select(p for p in Players).order_by(lambda p: p.support)],
    tags = [x.name for x in select(p for p in Players).order_by(lambda p: p.tags)])

with db_session:
    for i, player in enumerate(select(p for p in Players)):
        p_dict = {}
        for item, l in data.iteritems():
            try:
                p_dict[item] = l.index(player.name)
            except Exception as e:
                print e
                p_dict[item] = None
        Ranks(player_id=player, **p_dict)
        if not i%100:
            print "Finished  {}".format(i)

    commit()
