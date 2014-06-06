from db import Session, AllTimeStats, DailyStats
import timeit
import functools

def generate_rankings(query):
    ca
def main():
    session = Session()
    all_stats = session.query(DailyStats).is_current().all()
    print all_stats



if __name__ == "__main__":
    main()