from apscheduler.schedulers.background import BackgroundScheduler
from parsers import get_listing_count
from database import SessionLocal
from models import SearchQuery, SearchStatistic
from datetime import datetime

def update_statistics():
    db = SessionLocal()
    queries = db.query(SearchQuery).all()
    for query in queries:
        count = get_listing_count(query.query, query.region)
        stat = SearchStatistic(search_query_id=query.id, timestamp=datetime.utcnow(), count=count)
        db.add(stat)
    db.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(update_statistics, 'interval', minutes=60)
scheduler.start()
