from datetime import datetime
from config import db


class Streamer(db.Model):
    __tablename__ = "streamer"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    platform = db.Column(db.String(64))
    streaming_url = db.Column(db.String(300))
    profile_image = db.Column(db.String(300))

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "platform": self.platform,
            "streaming_url": self.streaming_url,
            "profile_image": self.profile_image,
        }
