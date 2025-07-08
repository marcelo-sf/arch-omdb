from sqlalchemy.orm import declarative_base

Base = declarative_base()
from sqlalchemy import (
    Column, String, Integer, Text, SmallInteger,
    JSON, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


def current_time():
    return datetime.now(timezone.utc)


class Movie(Base):
    __tablename__ = "movies"

    imdb_id = Column(String(15), primary_key=True)
    title = Column(String(255), nullable=False)
    year = Column(Integer, nullable=True)
    metadata_json = Column("metadata", JSON, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=current_time,
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=current_time,
        onupdate=current_time,
        nullable=False
    )

    reviews = relationship(
        "Review",
        back_populates="movie",
        cascade="all, delete-orphan"
    )


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    imdb_id = Column(
        String(15),
        ForeignKey("movies.imdb_id", ondelete="CASCADE"),
        nullable=False
    )
    user_opinion = Column(Text, nullable=False)
    user_rating = Column(SmallInteger, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=current_time,
        nullable=False
    )

    movie = relationship("Movie", back_populates="reviews")