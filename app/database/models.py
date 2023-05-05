from os import environ

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create the engine to connect to the database
engine = create_engine(environ.get("DATABASE_URL"), echo=True)

# create a declarative base
Base = declarative_base()

Session = sessionmaker(bind=engine)
db_session = Session()


# Define the schema
class Hunts(Base):
    __tablename__ = "hunts"

    hunt_id = Column(Integer, primary_key=True)
    organizer_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    photo_url = Column(String)
    created_at = Column(DateTime, server_default="now()")
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)


class Treasures(Base):
    __tablename__ = "treasures"

    treasure_id = Column(Integer, primary_key=True)
    hunt_id = Column(
        Integer, ForeignKey("hunts.hunt_id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String, nullable=False)
    win_message = Column(String, nullable=False)
    photo_url = Column(String)
    riddle_id = Column(Integer, ForeignKey("riddles.riddle_id", ondelete="CASCADE"))


class Winners(Base):
    __tablename__ = "winners"

    treasure_id = Column(
        Integer, primary_key=True
    )  # , ForeignKey('treasures.treasure_id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, nullable=False)


class Riddles(Base):
    __tablename__ = "riddles"

    riddle_id = Column(Integer, primary_key=True)
    riddle = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    hints = Column(String)
