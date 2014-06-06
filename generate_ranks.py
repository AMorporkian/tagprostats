from sqlalchemy import func
from sqlalchemy.orm import aliased

from db import Session, AllTimeStats, DailyStats, MonthlyStats, WeeklyStats, \
    Stats, Ranking


session = Session()


def generate_rankings(query, t):
    for stat in query.filter(t.ranking == None):
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
        s1 = aliased(Stats)
        print "   * Doing {}".format(s)
        subq = session.query(
            t.id.label("rid"),
            func.rank().over(order_by=column.desc()).label('rank')).select_from(t).subquery("r")
        update = Ranking.__table__.update().values({column: subq.c.rank}).where(
            Ranking.id == subq.c.rid)
        session.execute(update)

    print "Committing..."
    session.commit()


def main():
    all_stats = session.query(AllTimeStats).current()
    monthly_stats = session.query(MonthlyStats).current()
    weekly_stats = session.query(WeeklyStats).current()
    daily_stats = session.query(DailyStats).current()
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