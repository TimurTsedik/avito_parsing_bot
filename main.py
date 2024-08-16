from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, SearchQuery, SearchStatistic
from parsers import get_listing_count
from scheduler import scheduler
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Создаем зависимость для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/add/")
def add_search(query: str, region: str, db: Session = Depends(get_db)):
    # Создаем запись для нового запроса
    search_query = SearchQuery(query=query, region=region)
    db.add(search_query)
    db.commit()
    db.refresh(search_query)

    # Получаем текущее количество объявлений для сохранения начальной статистики
    count = get_listing_count(query, region)
    initial_stat = SearchStatistic(
        search_query_id=search_query.id,
        timestamp=datetime.utcnow(),
        count=count
    )
    db.add(initial_stat)
    db.commit()

    return {"id": search_query.id}


@app.get("/stat/{id}")
def get_statistics(id: int, db: Session = Depends(get_db)):
    search_query = db.query(SearchQuery).filter(SearchQuery.id == id).first()
    if not search_query:
        raise HTTPException(status_code=404, detail="Search query not found")

    stats = db.query(SearchStatistic).filter(SearchStatistic.search_query_id == id).all()
    return {"query": search_query.query, "region": search_query.region, "statistics": stats}


# Запускаем планировщик прямо в модуле, чтобы он не запускался повторно
if not scheduler.running:
    scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()  # Останавливаем планировщик при выключении приложения
