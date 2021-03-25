from datetime import datetime
from config import db


class Streamer(db.Model):
    __tablename__ = "streamer"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    session_title = db.Column(db.String(64))
    start_date = db.Column(db.DateTime, default=datetime.utcnow)

    def json(self):
        return {
            "username": self.username,
            "session_title": self.session_title,
            "start_date": str(self.start_date)
        }
