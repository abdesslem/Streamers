#!/usr/bin/env python3
import datetime
import logging

import connexion

# from flask import g
from connexion import NoContent
from models.streamers import Streamer
from config import db
from providers.provider import Provider


# I used twith API if streamer doesnt exist in local DB
def get_streamer(username: str):
    db_streamer = Streamer.query.filter(Streamer.username == username).one_or_none()
    if db_streamer:
        return db_streamer.json()
    else:
        streaming_provider = Provider()
        provider_streamer = streaming_provider.get_user(username=username)
        if provider_streamer:
            return provider_streamer.json()
        else:
            return {"details": "Streamer not found"}, 404


def get_streamers():
    streamer_body = []
    streamers = Streamer.query.filter().all()
    for streamer in streamers:
        streamer_body.append(streamer.json())
    return streamer_body


def create_streamer(streamer):
    streamer_instance = Streamer(
        platform=streamer.get("platform"),
        username=streamer.get("username"),
        streaming_url=streamer.get("streaming_url"),
        profile_image=streamer.get("profile_image"),
    )
    db.session.add(streamer_instance)
    db.session.commit()
    return streamer_instance.json()


def delete_streamer(username: str):
    streamer = Streamer.query.filter(Streamer.username == username).one_or_none()
    if streamer:
        db.session.delete(streamer)
        db.session.commit()
        return NoContent
    else:
        return {"details": "Streamer not found"}, 404