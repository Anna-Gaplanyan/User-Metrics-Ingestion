import os
import time
import logging
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, ForeignKey, Index
)
from sqlalchemy.dialects.postgresql import TIMESTAMP as TIMESTAMPTZ
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.exc import OperationalError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMPTZ(timezone=True), default=func.now())
    sessions = relationship("Session", back_populates="user")


class Session(Base):
    __tablename__ = "sessions"
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    start_time = Column(TIMESTAMPTZ(timezone=True), nullable=False)
    end_time = Column(TIMESTAMPTZ(timezone=True), nullable=True)
    device_info = Column(String(255), nullable=True)
    __table_args__ = (Index("idx_session_user_id", "user_id"),)
    user = relationship("User", back_populates="sessions")
    metrics = relationship("Metric", back_populates="session")


class Metric(Base):
    __tablename__ = "metrics"
    metric_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id"), nullable=False)
    timestamp = Column(TIMESTAMPTZ(timezone=True), nullable=False)
    talked_time = Column(Integer, nullable=True)
    microphone_used = Column(Boolean, nullable=True)
    speaker_used = Column(Boolean, nullable=True)
    voice_sentiment = Column(String(50), nullable=True)
    __table_args__ = (Index("idx_metrics_session_id", "session_id"),)
    session = relationship("Session", back_populates="metrics")


def create_database(max_attempts=5):
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("The DATABASE_URL environment variable is not set.")

    attempt_count = 0
    while attempt_count < max_attempts:
        try:
            engine = create_engine(database_url)
            connection = engine.connect()
            logging.info("Database connection established successfully.")

            Base.metadata.create_all(engine)

            return sessionmaker(bind=engine)
        except OperationalError as e:
            attempt_count += 1
            logging.warning(
                f"Database connection attempt {attempt_count}/{max_attempts} failed: {e}"
            )
            time.sleep(10)

    raise Exception("Failed to connect to the database after several attempts.")


if __name__ == "__main__":
    SessionLocal = create_database()
