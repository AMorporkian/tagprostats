import time
from db import Session, AllTimeStats, DailyStats, MonthlyStats, WeeklyStats, \
    Stats, Ranking
import timeit
import functools

session = Session()
def generate_rankings(query, t):
    for stat in query:
        if stat.ranking is None:
            stat.ranking = Ranking()

    columns = ['captures', 'disconnects', 'drops', 'games', 'grabs', 'hold',
               'hours', 'losses', 'popped', 'prevent', 'returns', 'support',
               'tags', 'wins', 'captures_per_hour', 'disconnects_per_hour',
               'drops_per_hour', 'games_per_hour', 'grabs_per_hour',
               'hold_per_hour', 'losses_per_hour', 'popped_per_hour',
               'prevent_per_hour', 'returns_per_hour', 'support_per_hour',
               'tags_per_hour', 'wins_per_hour', 'captures_per_game',
               'disconnects_per_game', 'drops_per_game', 'grabs_per_game',
               'hold_per_game', 'losses_per_game', 'popped_per_game',
               'prevent_per_game', 'returns_per_game', 'support_per_game',
               'tags_per_game', 'wins_per_game']

    for s in columns:
        column = getattr(t, s)
        print "   * Doing {}".format(s)
        for i, stat in enumerate(query.order_by(column.desc())):
            setattr(stat.ranking, s, i)
    print "Committing..."
    session.commit()


def main():
    all_stats = session.query(AllTimeStats).current()
    monthly_stats = session.query(MonthlyStats).current()
    weekly_stats = session.query(WeeklyStats).current()
    daily_stats =  session.query(DailyStats).current()
    print "Generating all-time rankings..."
    generate_rankings(all_stats, AllTimeStats)
    print "Generating monthly rankings..."
    generate_rankings(monthly_stats, MonthlyStats)
    print "Generating weekly rankings..."
    generate_rankings(weekly_stats, WeeklyStats)
    print "Generating daily rankings..."
    generate_rankings(daily_stats, DailyStats)

if __name__ == "__main__":
    main()