from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import os
import threading
import logging
from models import User, Session, Metric, Base

app = Flask(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s:%(message)s",
    handlers=[
        logging.FileHandler("ingestion.log"),
        logging.StreamHandler()
    ]
)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.metadata.create_all(bind=engine)

def ingest_metric_data(metrics_data):
    db_session = SessionLocal()
    try:
        user = db_session.query(User).filter_by(email=metrics_data["user_email"]).first()
        if not user:
            user = User(name=metrics_data["user_name"], email=metrics_data["user_email"])
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)

        session = db_session.query(Session).filter_by(session_id=metrics_data["session_id"]).first()
        if not session:
            session = Session(
                user_id=user.user_id,
                start_time=metrics_data["start_time"],
                device_info=metrics_data["device_info"]
            )
            db_session.add(session)
            db_session.commit()
            db_session.refresh(session)

        metric = Metric(
            session_id=session.session_id,
            timestamp=metrics_data["timestamp"],
            talked_time=metrics_data["talked_time"],
            microphone_used=metrics_data["microphone_used"],
            speaker_used=metrics_data["speaker_used"],
            voice_sentiment=metrics_data["voice_sentiment"]
        )
        db_session.add(metric)
        db_session.commit()
    except (KeyError, ValueError, IntegrityError, SQLAlchemyError, Exception) as e:
        db_session.rollback()
        logging.error("Error during data ingestion: %s", str(e))
    finally:
        db_session.close()

@app.route("/ingest", methods=["POST"])
def ingest_data():
    metrics_data = request.json
    required_fields = [
        "user_id", "user_name", "user_email", "session_id", "start_time",
        "device_info", "timestamp", "talked_time", "microphone_used",
        "speaker_used", "voice_sentiment"
    ]
    if any(field not in metrics_data for field in required_fields):
        missing = [field for field in required_fields if field not in metrics_data]
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    threading.Thread(target=ingest_metric_data, args=(metrics_data,)).start()
    return jsonify({"status": "Data ingestion in progress"}), 202

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
