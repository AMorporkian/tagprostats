from pony.orm import *
from datetime import datetime

db = Database('sqlite', 'players.sqlite', create_db=True)

class Players(db.Entity):
    _table_ = "profile_stats"

    id = PrimaryKey(int, auto=True)
    last_updated = Required(datetime)
    name = Required(unicode, 50)
    server = Optional(unicode, 25)
    profile_string = Required(unicode, 30)
    captures = Required(int)
    disconnects = Required(int)
    drops = Required(int)
    games = Required(int)
    grabs = Required(int)
    hold = Required(int)
    hours = Required(float)
    losses = Required(int)
    non_return_tags = Required(int)
    popped = Required(int)
    prevent = Required(int)
    returns = Required(int)
    support = Required(int)
    tags = Required(int)
    wins = Required(int)
    ranks = Optional("Ranks")

class Ranks(db.Entity):
    player_id = Required(Players)
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
    wins = Optional(int)

db.generate_mapping(create_tables=True)