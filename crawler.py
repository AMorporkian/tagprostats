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
    s = "http://tagpro-origin.koalabeast.com/profile/{}".format(player.profile_string)
    page = urllib2.urlopen(s).read()
    #print page.text
    tree = html.fromstring(page)
    t = tree.xpath('/html/body/article/table[2]')
    data = dict(zip(('tags', 'popped', 'grabs', 'drops', 'hold', 'captures', 'prevent', 'returns', 'support'), [x.text for x in t[0][4][1:]]))
    player.set(**data)
    c+=1
    if not c%100:
        print "{}/{} done.".format(c, total)

with db_session:
    players = list(select(x for x in Players))
    total = len(players)
    p = Pool(50)
    res = p.map_async(update_player, players)
    gevent.wait([res])
    print "Committing..."
    commit()
    print "Done."