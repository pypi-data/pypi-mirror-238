"""
This is the main entry point for the Podigee Connector.
"""

import json
import os
from loguru import logger
from .connector import PodigeeConnector


def load_env_var(var_name: str) -> str:
    """
    Load environment variable or throw error
    """
    var = os.environ.get(var_name)
    if var is None or var == "":
        raise ValueError(f"Environment variable {var_name} must be set.")
    return var


def main():
    """
    Main entry point for the Podigee Connector.
    """
    base_url = load_env_var("PODIGEE_BASE_URL")
    podcast_id = load_env_var("PODCAST_ID")

    # This can be empty, in which case the username and password will be used
    podigee_session_v5 = os.environ.get("PODIGEE_SESSION_V5")

    if podigee_session_v5:
        connector = PodigeeConnector(
            base_url=base_url,
            podcast_id=podcast_id,
            podigee_session_v5=podigee_session_v5,
        )
    else:
        # Use username and password to log in
        username = load_env_var("PODIGEE_USERNAME")
        password = load_env_var("PODIGEE_PASSWORD")
        connector = PodigeeConnector.from_credentials(
            base_url=base_url,
            podcast_id=podcast_id,
            username=username,
            password=password,
        )

    podcast_analytics = connector.podcast_analytics()
    logger.info("Podcast Analytics = {}", json.dumps(podcast_analytics, indent=4))

    episodes = connector.episodes()
    logger.info("Episodes = {}", json.dumps(episodes, indent=4))

    for episode in episodes:
        episode_id = episode["id"]
        episode_analytics = connector.episode_analytics(episode_id)
        logger.info(
            "Episode {} = {}", episode_id, json.dumps(episode_analytics, indent=4)
        )


if __name__ == "__main__":
    main()
