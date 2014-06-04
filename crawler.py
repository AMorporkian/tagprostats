from datetime import datetime
from gevent import monkey
monkey.patch_socket()
import gevent
from lxml import html
import urllib2
from db import Players, db_session, commit, select, sql_debug, Monthly, Weekly, \
    Daily
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
    all = 4
    monthly = 3
    weekly = 2
    daily = 1
    def extract_data(z):
        data = dict(zip(('tags', 'popped', 'grabs', 'drops', 'hold', 'captures', 'prevent', 'returns', 'support'), [x.text for x in t[0][z][1:]]))
        data2 = dict(zip(('games', 'wins', 'losses', 'disconnects', 'hours'), [x.text for x in t2[0][z][2:7]]))
        data = dict(data.items()+data2.items())
        per_stat_cols = ('captures', 'drops', 'grabs', 'hold',
                         'losses', 'popped', 'prevent', 'returns',
                         'support', 'tags', 'wins')
        h_stats = {k+"_per_hour": float(data[k])/float(data['hours']) for k in per_stat_cols if float(data['hours']) > 0}
        g_stats = {k+"_per_game": float(data[k])/float(data['games']) for k in per_stat_cols if float(data['games']) > 0}
        return dict(data.items()+h_stats.items()+g_stats.items())
    player.set(last_updated=datetime.now(), **extract_data(all))
    if player.monthly is not None:
        player.monthly.set(**extract_data(monthly))
    else:
        Monthly(player=player, **extract_data(monthly))
    if player.weekly is not None:
        player.weekly.set(**extract_data(weekly))
    else:
        Weekly(player=player, **extract_data(weekly))
    if player.daily is not None:
        player.daily.set(**extract_data(daily))
    else:
        Daily(player=player, **extract_data(daily))
    c+=1
    if not c%100:
        print "{}/{} done.".format(c, total)

with db_session:
    players = select(x for x in Players)
    p = Pool(10)
    total = len(players)
    res = p.imap(update_player, players)
    gevent.wait([res])
    print "Committing..."
    commit()
    print "Done."
