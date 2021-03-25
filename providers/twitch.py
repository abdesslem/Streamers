import os
from typing import Optional

import requests
from werkzeug.exceptions import HTTPException

from models.streamers import Streamer


class Twitch:
    def __init__(self):
        self.platform = "Twitch"
        self.login_url = "https://id.twitch.tv/oauth2/token"
        self.api_url = "https://api.twitch.tv/helix"
        self.subscription_url = "https://api.twitch.tv/helix/eventsub/subscriptions"
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.access_token = self.get_token_from_twitch()
        self.subscription_secret = "test"

    def get_token_from_twitch(self) -> Optional[str]:
        response = requests.post(
            "{}?client_id={}&client_secret={}&grant_type=client_credentials".format(
                self.login_url, self.client_id, self.client_secret
            ),
            verify=False,
        )

        if response.ok:
            return response.json().get("access_token")

    def get_headers(self):
        return {
            "Authorization": "Bearer {}".format(self.access_token),
            "Client-Id": self.client_id,
        }

    def get_user(self, username: str) -> Streamer:
        response = requests.get(
            "{}/users?login={}".format(self.api_url, username),
            headers=self.get_headers(),
            verify=False,
        )

        if response.ok and (not self.is_empty_data(response)):
            data = response.json().get("data")[0]
            streamer = Streamer(
                platform=self.platform,
                username=data.get("login"),
                streaming_url="{}{}".format("twitch.tv/", data.get("login")),
                profile_image=data.get("profile_image_url"),
            )
            return streamer
    
    def is_empty_data(self, response):
        return True if not response.json().get("data") else False

    def follow_streamer(self, streamer_id: str):
        body = {
            "type": "stream.online",
            "version": "1",
            "condition": {
                "broadcaster_user_id": streamer_id
            },
            "transport": {
                "method": "webhook",
                "callback": self.callback_url,
                "secret": self.subscription_secret
            }
        }

        response = requests.get(
            self.subscription_url,
            headers=self.get_headers(),
            json=body,
            verify=False,
        )
