from os import environ

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create the engine to connect to the database
engine = create_engine(environ.get("DATABASE_URL"), echo=True)

# create a declarative base
Base = declarative_base()

# Db session
Session = sessionmaker(bind=engine)
db_session = Session()


class Hunts(Base):
    __tablename__ = "hunts"
    hunt_id = Column(Integer, primary_key=True)
    organizer_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    photo_url = Column(Text)
    created_at = Column(DateTime, server_default="NOW()")
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)


class Treasures(Base):
    __tablename__ = "treasures"
    treasure_id = Column(Integer, primary_key=True)
    treasure_secret = Column(Text, unique=True, nullable=False)
    hunt_id = Column(
        Integer, ForeignKey("hunts.hunt_id", ondelete="CASCADE"), nullable=False
    )
    title = Column(Text, nullable=False)
    description = Column(Text)
    win_message = Column(Text, nullable=False)
    photo_url = Column(Text)
    riddle_id = Column(Integer, ForeignKey("riddles.riddle_id", ondelete="CASCADE"))


class HuntParticipants(Base):
    __tablename__ = "hunt_participants"
    treasure_id = Column(
        Integer,
        ForeignKey("treasures.treasure_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    join_date = Column(DateTime, server_default="NOW()")


class Winners(Base):
    __tablename__ = "winners"
    treasure_id = Column(
        Integer,
        ForeignKey("treasures.treasure_id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id = Column(Integer, nullable=False)
    win_date = Column(DateTime, server_default="NOW()")


class Riddles(Base):
    __tablename__ = "riddles"
    riddle_id = Column(Integer, primary_key=True, autoincrement=True)
    riddle = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    hints = Column(Text)
