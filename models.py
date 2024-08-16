from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class SearchQuery(Base):
    __tablename__ = 'search_queries'
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    region = Column(String, index=True)
    statistics = relationship("SearchStatistic", back_populates="search_query")

class SearchStatistic(Base):
    __tablename__ = 'search_statistics'
    id = Column(Integer, primary_key=True, index=True)
    search_query_id = Column(Integer, ForeignKey('search_queries.id'))
    timestamp = Column(DateTime)
    count = Column(Integer)
    search_query = relationship("SearchQuery", back_populates="statistics")
