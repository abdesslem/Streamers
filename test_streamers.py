import os
import tempfile

import pytest

from app import connex_app
import config


@pytest.fixture
def client():
    db_fd, connex_app.app.config['DATABASE'] = tempfile.mkstemp()
    connex_app.app.config['TESTING'] = True

    with connex_app.app.test_client() as client:
        with connex_app.app.app_context():
            config.db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(connex_app.app.config['DATABASE'])

def test_get_create_streamer(client):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    body = {
        "platform": "Twitch",
        "profile_image": "string",
        "streaming_url": "twitch.tv/dummy_man",
        "username": "zold90"
    }
    rv = client.post('/streamers', headers=headers, json=body)
    assert rv.status_code == 200


def test_get_streamers(client):
    rv = client.get('/streamers')
    assert rv.status_code == 200


def test_get_one_streamer_success(client):
    rv = client.get('/streamers/zold90')
    assert rv.status_code == 200


def test_get_one_streamer_notfound(client):
    rv = client.get('/streamers/1337dummydummy1234')
    assert rv.status_code == 404


def test_delete_existing_streamer(client):
    rv = client.delete('/streamers/zold90')
    assert rv.status_code == 204


def test_delete_not_existing_streamer(client):
    rv = client.delete('/streamers/nope')
    assert rv.status_code == 404