from discord import app_commands, Interaction
from urllib.parse import urlparse
import logging
from httpx import AsyncClient
from db import Database
from schemas import SteamAppGame

handler = logging.getLogger('discord')
handler.setLevel(logging.INFO)


def get_steam_url(game_id: str) -> str:
    return f"https://store.steampowered.com/app/{game_id}/"


class SteamClient:
    def __init__(self):
        self.http_client = AsyncClient(
            base_url="https://store.steampowered.com")

    async def get_game_details(self, app_id: str):
        try:
            response = await self.http_client.get(f"/api/appdetails?appids={app_id}")
            response.raise_for_status()
        except Exception as e:
            handler.error(
                f"Error fetching game details for app ID {app_id}: {e}")
            return None
        raw_app_game = response.json()
        app_game = SteamAppGame(
            app_id=int(app_id),
            name=raw_app_game[app_id]['data']['name']
        )
        return app_game


class SteamCommands(app_commands.Group):
    def __init__(self, db: Database):
        self.steam_client = SteamClient()
        self.db = db
        super().__init__(name="steam", description="Commands related to Steam.")

    @app_commands.command(name="add", description="add steam games to the wishlist")
    async def add(self, interaction: Interaction, game_link: str):
        if "store.steampowered.com/app/" not in game_link:
            await interaction.response.send_message("Please provide a valid Steam game link.")
            return
        parsed_url = urlparse(game_link)
        game_id = parsed_url.path.split("/")[2]
        handler.info(
            f"Adding {game_id} to wishlist for user {interaction.user}")
        steam_app_game = await self.steam_client.get_game_details(game_id)

        user = await self.db.upsert_user(str(interaction.user))
        await self.db.add_steam_game(
            game_app_id=steam_app_game.app_id,
            game_name=steam_app_game.name,
            creator=int(user['id'])
        )

        if steam_app_game:
            await interaction.response.send_message(f"Adding [{steam_app_game.name}]({get_steam_url(steam_app_game.app_id)}) to the wishlist, thanks {interaction.user.mention}!")
        else:
            await interaction.response.send_message(f"Could not fetch game details for app ID {game_id}, but added to wishlist anyway!")

    @app_commands.command(name="list", description="list steam games to the wishlist")
    async def lst(self, interaction: Interaction):
        handler.info(f"Listing wishlist for user {interaction.user}")
        games = await self.db.get_steam_games()
        if not games:
            await interaction.response.send_message("The wishlist is currently empty.")
            return
        await interaction.response.send_message(f"Here are your steam games on the wishlist: " + ", ".join(str(game) for game in games))

    @app_commands.command(name="delete", description="delete a steam games to the wishlist")
    async def delete(self, interaction: Interaction, game_id: str):
        handler.info(
            f"Removing {game_id} from wishlist for user {interaction.user}")
        result = await self.db.delete_steam_game(int(game_id))
        if not result:
            await interaction.response.send_message(f"Could not find game with App ID {game_id} in the wishlist.")
            return
        await interaction.response.send_message(f":boom: Removed {get_steam_url(game_id)} from the wishlist")
