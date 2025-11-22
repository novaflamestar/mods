from functools import lru_cache
import asyncpg
from config import get_config
from logging import getLogger

handler = getLogger('discord')


@lru_cache(maxsize=1)
async def init_db():
    # Placeholder for database initialization logic
    config = get_config()
    handler.info("Initializing database connection...")
    conn = await asyncpg.connect(
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        database=config.POSTGRES_DB,
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
    )
    return conn


class Database:
    def __init__(self, connection):
        self.connection = connection

    async def add_user(self, username: str):
        handler.info(f"Adding user {username} to the database.")
        result = await self.connection.fetchrow(
            "INSERT INTO users (username) VALUES ($1) RETURNING *;",
            username,
        )
        handler.info(f"User {username} added successfully: {result}")
        return result

    async def get_user(self, username: str):
        handler.info(f"Fetching user {username} from the database.")
        result = await self.connection.fetchrow(
            "SELECT * FROM users WHERE username = $1;",
            username,
        )
        return result

    async def upsert_user(self, username: str):
        result = await self.get_user(username)
        if result is None:
            result = await self.add_user(username)
        return result

    async def get_user_stats(self, username: str):
        handler.info(f"Fetching stats for user {username}.")
        result = await self.connection.fetchrow(
            "SELECT * FROM users LEFT JOIN bans ON users.id = bans.user_id where users.username = $1;",
            username,
        )
        handler.info(f"Stats for user {username}: {result}")
        return result

    async def get_users(self):
        pass

    async def add_steam_game(self, game_id: str, game_app_id: str, game_name: str, creator: int):
        pass

    async def get_steam_games(self):
        pass

    async def delete_steam_game(self, game_id: str):
        pass

    async def init_stats(self, user_id: int):
        handler.info(f"Initializing stats for user ID {user_id}.")
        try:
            await self.connection.execute(
                "INSERT INTO bans (user_id, target_bans, source_bans) VALUES ($1, 0, 0) ON CONFLICT (user_id) DO NOTHING;",
                user_id,
            )
        except Exception as e:
            handler.error(
                f"Error initializing stats for user ID {user_id}: {e}")
            raise e

    async def increment_target_bans(self, user_id: int):
        handler.info(f"Incrementing target bans for user ID {user_id}.")
        try:
            await self.connection.execute(
                "INSERT INTO bans (user_id, target_bans, source_bans) VALUES ($1, 1, 0) ON CONFLICT (user_id) DO UPDATE SET target_bans = bans.target_bans + 1;",
                user_id,
            )
        except Exception as e:
            handler.error(
                f"Error incrementing target bans for user ID {user_id}: {e}")
            raise e

    async def increment_source_bans(self, user_id: int):
        handler.info(f"Incrementing target bans for user ID {user_id}.")
        try:
            await self.connection.execute(
                "INSERT INTO bans (user_id, target_bans, source_bans) VALUES ($1, 0, 1) ON CONFLICT (user_id) DO UPDATE SET source_bans = bans.source_bans + 1;",
                user_id,
            )
        except Exception as e:
            handler.error(
                f"Error incrementing source bans for user ID {user_id}: {e}")
            raise e
