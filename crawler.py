from gevent import monkey
monkey.patch_socket()
import gevent
from lxml import html
import urllib2
from db import Players, db_session, commit, select, sql_debug
from gevent.pool import Pool
#sql_debug(True)
c = 0

def update_player(player):
    global c, total
    s = "http://tagpro-pi.koalabeast.com/profile/{}".format(player.profile_string)
    page = urllib2.urlopen(s).read()
    #print page.text
    tree = html.fromstring(page)
    t = tree.xpath('/html/body/article/table[2]')
    t2 = tree.xpath('/html/body/article/table[1]')
    data = dict(zip(('tags', 'popped', 'grabs', 'drops', 'hold', 'captures', 'prevent', 'returns', 'support'), [x.text for x in t[0][4][1:]]))
    data2 = dict(zip(('games', 'wins', 'losses', 'disconnects', 'hours'), [x.text for x in t2[0][4][2:7]]))
    data = dict(data.items()+data2.items())
    """

    captures_per_hour = Optional(float)
    disconnects_per_hour = Optional(float)
    drops_per_hour = Optional(float)
    grabs_per_hour = Optional(float)
    hold_per_hour = Optional(float)
    losses_per_hour = Optional(float)
    popped_per_hour = Optional(float)
    prevent_per_hour = Optional(float)
    returns_per_hour = Optional(float)
    support_per_hour = Optional(float)
    tags_per_hour = Optional(float)
    wins_per_hour = Optional(float)
    """
    per_stat_cols = ('captures', 'drops', 'grabs', 'hold', 
                     'losses', 'popped', 'prevent', 'returns',
                     'support', 'tags', 'wins')
    h_stats = {k+"_per_hour": float(data[k])/float(data['hours']) for k in per_stat_cols if float(data['hours']) > 0}
    g_stats = {k+"_per_game": float(data[k])/float(data['games']) for k in per_stat_cols if float(data['games']) > 0}
    data = dict(data.items()+h_stats.items()+g_stats.items())
    player.set(**data)
    c+=1
    if not c%100:
        print "{}/{} done.".format(c, total)

with db_session:
    players = select(x for x in Players)
    p = Pool(20)
    total = len(players)
    res = p.imap(update_player, players)
    gevent.wait([res])
    print "Committing..."
    commit()
    print "Done."
