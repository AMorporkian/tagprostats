from datetime import date, datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Unicode, Float, \
    Date, create_engine
from sqlalchemy.orm import relationship, sessionmaker, Query, query, Mapper, \
    backref
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"

    profile_string = Column(Unicode, primary_key=True)
    last_updated = Column(DateTime)
    name = Column(Unicode)
    server = Column(Unicode)

    all_time_stats = relationship("AllTimeStats", uselist=False, backref="players")
    monthly_stats = relationship("MonthlyStats")
    weekly_stats = relationship("WeeklyStats")
    daily_stats = relationship("DailyStats")


class Stats(Base):
    __tablename__ = "stats"
    
    id = Column(Integer, primary_key=True)
    player = Column(Unicode, ForeignKey('players.profile_string'))

    captures = Column(Integer)
    disconnects = Column(Integer)
    drops = Column(Integer)
    games = Column(Integer)
    grabs = Column(Integer)
    hold = Column(Integer)
    hours = Column(Float)
    losses = Column(Integer)
    popped = Column(Integer)
    prevent = Column(Integer)
    returns = Column(Integer)
    support = Column(Integer)
    tags = Column(Integer)
    wins = Column(Integer)

    captures_per_hour = Column(Float)
    disconnects_per_hour = Column(Float)
    drops_per_hour = Column(Float)
    games_per_hour = Column(Float)
    grabs_per_hour = Column(Float)
    hold_per_hour = Column(Float)
    losses_per_hour = Column(Float)
    popped_per_hour = Column(Float)
    prevent_per_hour = Column(Float)
    returns_per_hour = Column(Float)
    support_per_hour = Column(Float)
    tags_per_hour = Column(Float)
    wins_per_hour = Column(Float)

    captures_per_game = Column(Float)
    disconnects_per_game = Column(Float)
    drops_per_game = Column(Float)
    grabs_per_game = Column(Float)
    hold_per_game = Column(Float)
    losses_per_game = Column(Float)
    popped_per_game = Column(Float)
    prevent_per_game = Column(Float)
    returns_per_game = Column(Float)
    support_per_game = Column(Float)
    tags_per_game = Column(Float)
    wins_per_game = Column(Float)

    ranking = relationship("Ranking", uselist=False, backref=backref("stats",
                           enable_typechecks=False))

class AllTimeStats(Stats):
    __tablename__ = "all_time_stats"
    __mapper_args__ = {'polymorphic_identity': 'all_time_stats'}

    id = Column(Integer, ForeignKey('stats.id'), primary_key=True)


class MonthlyStats(Stats):
    __tablename__ = "monthly_stats"
    __mapper_args__ = {'polymorphic_identity':'monthly_stats',}

    id = Column(Integer, ForeignKey('stats.id'), primary_key=True)
    year = Column(Integer)
    month_number = Column(Integer)


class WeeklyStats(Stats):
    __tablename__ = "weekly_stats"
    __mapper_args__ = {'polymorphic_identity':'weekly_stats',}

    id = Column(Integer, ForeignKey('stats.id'), primary_key=True)
    year = Column(Integer)
    week_number = Column(Integer)

class DailyStats(Stats):
    __tablename__ = "daily_stats"
    __mapper_args__ = {'polymorphic_identity':'daily_stats'}

    id = Column(Integer, ForeignKey('stats.id'), primary_key=True)
    date = Column(Date)

class Ranking(Base):
    __tablename__ = "rankings"
    id = Column(Integer, primary_key=True)
    parent = Column(Integer, ForeignKey('stats.id'))

    captures = Column(Integer)
    disconnects = Column(Integer)
    drops = Column(Integer)
    games = Column(Integer)
    grabs = Column(Integer)
    hold = Column(Integer)
    hours = Column(Integer)
    losses = Column(Integer)
    popped = Column(Integer)
    prevent = Column(Integer)
    returns = Column(Integer)
    support = Column(Integer)
    tags = Column(Integer)
    wins = Column(Integer)

    captures_per_hour = Column(Float)
    disconnects_per_hour = Column(Float)
    drops_per_hour = Column(Float)
    games_per_hour = Column(Float)
    grabs_per_hour = Column(Float)
    hold_per_hour = Column(Float)
    losses_per_hour = Column(Float)
    popped_per_hour = Column(Float)
    prevent_per_hour = Column(Float)
    returns_per_hour = Column(Float)
    support_per_hour = Column(Float)
    tags_per_hour = Column(Float)
    wins_per_hour = Column(Float)

    captures_per_game = Column(Float)
    disconnects_per_game = Column(Float)
    drops_per_game = Column(Float)
    grabs_per_game = Column(Float)
    hold_per_game = Column(Float)
    losses_per_game = Column(Float)
    popped_per_game = Column(Float)
    prevent_per_game = Column(Float)
    returns_per_game = Column(Float)
    support_per_game = Column(Float)
    tags_per_game = Column(Float)
    wins_per_game = Column(Float)

class Leaderboard(Base):
    __tablename__ = 'leaderboards'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)

    captures = Column(Unicode, ForeignKey('players.profile_string'))
    disconnects = Column(Unicode, ForeignKey('players.profile_string'))
    drops = Column(Unicode, ForeignKey('players.profile_string'))
    games = Column(Unicode, ForeignKey('players.profile_string'))
    grabs = Column(Unicode, ForeignKey('players.profile_string'))
    hold = Column(Unicode, ForeignKey('players.profile_string'))
    hours = Column(Unicode, ForeignKey('players.profile_string'))
    losses = Column(Unicode, ForeignKey('players.profile_string'))
    popped = Column(Unicode, ForeignKey('players.profile_string'))
    prevent = Column(Unicode, ForeignKey('players.profile_string'))
    returns = Column(Unicode, ForeignKey('players.profile_string'))
    support = Column(Unicode, ForeignKey('players.profile_string'))
    tags = Column(Unicode, ForeignKey('players.profile_string'))
    wins = Column(Unicode, ForeignKey('players.profile_string'))

    captures_per_hour = Column(Unicode, ForeignKey('players.profile_string'))
    disconnects_per_hour = Column(Unicode, ForeignKey('players.profile_string'))
    drops_per_hour = Column(Unicode, ForeignKey('players.profile_string'))
    games_per_hour = Column(Unicode, ForeignKey('players.profile_string'))
    grabs_per_hour = Column(Unicode, ForeignKey('players.profile_string'))
    hold_per_hour = Column(Unicode, ForeignKey('players.profile_string'))
    losses_per_hour = Column(Unicode, ForeignKey('players.profile_string'))
    popped_per_hour = Column(Unicode, ForeignKey('players.profile_string'))
    prevent_per_hour = Column(Unicode, ForeignKey('players.profile_string'))
    returns_per_hour = Column(Unicode, ForeignKey('players.profile_string'))
    support_per_hour = Column(Unicode, ForeignKey('players.profile_string'))
    tags_per_hour = Column(Unicode, ForeignKey('players.profile_string'))
    wins_per_hour = Column(Unicode, ForeignKey('players.profile_string'))

    captures_per_game = Column(Unicode, ForeignKey('players.profile_string'))
    disconnects_per_game = Column(Unicode, ForeignKey('players.profile_string'))
    drops_per_game = Column(Unicode, ForeignKey('players.profile_string'))
    grabs_per_game = Column(Unicode, ForeignKey('players.profile_string'))
    hold_per_game = Column(Unicode, ForeignKey('players.profile_string'))
    losses_per_game = Column(Unicode, ForeignKey('players.profile_string'))
    popped_per_game = Column(Unicode, ForeignKey('players.profile_string'))
    prevent_per_game = Column(Unicode, ForeignKey('players.profile_string'))
    returns_per_game = Column(Unicode, ForeignKey('players.profile_string'))
    support_per_game = Column(Unicode, ForeignKey('players.profile_string'))
    tags_per_game = Column(Unicode, ForeignKey('players.profile_string'))
    wins_per_game = Column(Unicode, ForeignKey('players.profile_string'))

class Current(Query):
    def _get_models(self):
        """Returns the query's underlying model classes."""
        if hasattr(self, 'attr'):
            # we are dealing with a subquery
            return [self.attr.target_mapper]
        else:
            return [
                d['expr']
                for d in self.column_descriptions
                if issubclass(d['expr'], Base)]

    def current(self):
        model_class = self._get_models()[0]
        date = datetime.today().date()
        if model_class is DailyStats:
            return self.filter(DailyStats.date == date)
        elif model_class is MonthlyStats:
            return self.filter(MonthlyStats.month_number == date.month,
                               MonthlyStats.year == date.year)
        elif model_class is WeeklyStats:
            return self.filter(WeeklyStats.week_number == date.isocalendar()[1],
                               WeeklyStats.year == date.year)
        elif model_class is AllTimeStats:
            return self


engine = create_engine('postgresql://postgres:test@localhost/tagprostats')  # , echo=True)
Session = sessionmaker(bind=engine, query_cls=Current)


if __name__ == "__main__":
    Base.metadata.create_all(engine)