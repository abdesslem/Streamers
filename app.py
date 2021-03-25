#!/usr/bin/env python3
import config
from models.streamers import Streamer

# Get the application instance
connex_app = config.connex_app

# Create DB
config.db.create_all()

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yaml")

if __name__ == "__main__":
    connex_app.run(debug=True)
