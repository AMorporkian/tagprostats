from datetime import datetime
import json
import random
import operator
import itertools
import subprocess

from gevent import monkey
from gevent.pool import Pool
from sqlalchemy.orm.exc import NoResultFound


monkey.patch_socket()
import gevent
from lxml import html
import urllib2
from db import Session, Player, AllTimeStats, MonthlyStats, WeeklyStats, \
    DailyStats
import ping

def update(obj, d):
    for k, v in d.iteritems():
        setattr(obj, k, v)

class Linker(object):
    servers = ["http://tagpro-centra.koalabeast.com",
               "http://tagpro-pi.koalabeast.com",
               "http://tagpro-chord.koalabeast.com",
               "http://tagpro-diameter.koalabeast.com",
               "http://tagpro-origin.koalabeast.com",
               "http://tagpro-diameter2.koalabeast.com",
               "http://tagpro-sphere.koalabeast.com",
               "http://tagpro-radius.koalabeast.com",
               "http://tagpro-orbit.koalabeast.com"]

    def ping(self, server):
        l = [float(line.rpartition('=')[-1][:-3]) for line in
         subprocess.check_output(['ping', '-c', '1', server[7:]]).splitlines()[
         1:-4]]
        return int(sum(l)/len(l))

    def get_stats(self):
        rdict = {}
        for server in self.servers:
            try:
                d = self.ping(server)
            except subprocess.CalledProcessError:
                print "Removing server {} because it is unpingable.".format(server)
                continue
            if d > 150:
                print "Removing server {} for high ping ({} ms)".format(server,
                                                                        d)
                continue
            players = json.load(urllib2.urlopen(server + "/stats"))['players']
            rdict[server] = players
        return rdict

    def generate_server_cycle(self):
        servers = []
        data = self.get_stats()
        for i, (server, count) in enumerate(sorted(data.items(),
                                    key=operator.itemgetter(1))):
            if count > 25:
                print 'Removing {} because it has >25 players on it.'.format(server)
                continue
            else:
                servers.extend([server]*int(len(data)/(i+1)))
        if len(servers) == 0:
            raise ValueError("All servers have more than 25 people on them (!)")
        random.shuffle(servers)
        print "Server cycle list:"
        print "\n".join(servers)
        print "Pool size: {}".format(len(servers))
        return len(servers), itertools.cycle(servers)

class Updater(gevent.Greenlet):
    def __init__(self, profile_strings):
        gevent.Greenlet.__init__(self)
        self.linker = Linker()
        pool_size, self.server_cycle = self.linker.generate_server_cycle()
        self.pool = Pool(50)
        self.profile_strings = profile_strings
        self.session = Session()
        self.count = 0
        self.total = len(self.profile_strings)

    def _run(self):
        while len(self.profile_strings) > 0:
            ps = self.profile_strings.pop()
            self.pool.wait_available()
            self.pool.add(gevent.spawn(self.update_player, ps,
                                       self.server_cycle.next()))

    def extract_data(self, table_1, table_2, tr_num):
        data = dict(zip(('tags', 'popped', 'grabs', 'drops', 'hold', 'captures',
                         'prevent', 'returns', 'support'),
                        [x.text for x in table_1[0][tr_num][1:]]))
        data2 = dict(zip(('games', 'wins', 'losses', 'disconnects', 'hours'),
                         [x.text for x in table_2[0][tr_num][2:7]]))
        data = dict(data.items() + data2.items())
        per_stat_cols = ('captures', 'drops', 'grabs', 'hold',
                         'losses', 'popped', 'prevent', 'returns',
                         'support', 'tags', 'wins')
        h_stats = {k + "_per_hour": float(data[k]) / float(data['hours']) for k
                   in per_stat_cols if float(data['hours']) > 0}
        g_stats = {k + "_per_game": float(data[k]) / float(data['games']) for k
                   in per_stat_cols if float(data['games']) > 0}
        return dict(data.items() + h_stats.items() + g_stats.items())

    def update_player(self, profile_string, server):
        server = server + "/profile/" + profile_string
        page = urllib2.urlopen(server).read()
        tree = html.fromstring(page)
        t = tree.xpath('/html/body/article/table[2]')
        t2 = tree.xpath('/html/body/article/table[1]')
        name = tree.xpath('/html/body/article/h3/text()')[0]
        all, monthly, weekly, daily = [self.extract_data(t, t2, x) for x in
                                       (4, 3, 2, 1)]
        try:
            player = self.session.query(Player).filter(Player.profile_string ==
                                                       profile_string).one()
        except NoResultFound:
            player = Player(name=name, profile_string=profile_string,
                            last_updated=datetime.now())
            self.session.add(player)

        if player.all_time_stats is None:
            player.all_time_stats = AllTimeStats(**all)
        else:
            update(player.all_time_stats, all)

        n = datetime.today().date()

        m = self.session.query(MonthlyStats).filter_by(
                player=player.profile_string,
                year=n.year,
                month_number=n.month)
        if m.count() == 1:
            update(m.one(), monthly)
        else:
            player.monthly_stats.append(MonthlyStats(
                month_number=n.month,
                year=n.year,
                **monthly))

        week_number = n.isocalendar()[1]

        w = self.session.query(WeeklyStats).filter_by(
                player=player.profile_string,
                year=n.year,
                week_number=week_number)
        if w.count() == 1:
            update(w.one(), weekly)
        else:
            player.weekly_stats.append(WeeklyStats(year=n.year,
                                                   week_number=week_number,
                                                   **weekly))


        d = self.session.query(DailyStats).filter_by(
                player=player.profile_string,
                date=n)
        if d.count() == 1:
            update(d.one(), daily)
        else:
            player.daily_stats.append(DailyStats(date=n, **daily))

        self.count += 1
        if not self.count % 100:
            print "{}/{} complete.".format(self.count, self.total)
            self.save()
    def save(self):
        print "Committing..."
        self.session.commit()
        print "Committed."
if __name__ == '__main__':
    with open('ids.txt') as f:
        players = [x.rstrip("\n") for x in f]
    crawler = Updater(players)
    crawler.run()
    crawler.save()
