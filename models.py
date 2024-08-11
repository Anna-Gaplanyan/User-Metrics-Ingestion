from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Index
)
from sqlalchemy.dialects.postgresql import TIMESTAMP as TIMESTAMPTZ
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

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
