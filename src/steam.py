from discord import app_commands, Interaction
from urllib.parse import urlparse
import logging

handler = logging.getLogger('discord')
handler.setLevel(logging.INFO)

def get_steam_url(game_id: str) -> str:
    return f"https://store.steampowered.com/app/{game_id}/"

wishlist = set()

class SteamCommands(app_commands.Group):
    def __init__(self):
        super().__init__(name="steam", description="Commands related to Steam.")
    
    @app_commands.command(name="add", description="add steam games to the wishlist")
    async def add(self, interaction: Interaction, game_link: str):
        if "store.steampowered.com/app/" not in game_link:
            await interaction.response.send_message("Please provide a valid Steam game link.")
            return
        parsed_url = urlparse(game_link)
        game_id = parsed_url.path.split("/")[2]
        handler.info(f"Adding {game_id} to wishlist for user {interaction.user}")
        wishlist.add(game_id)
        await interaction.response.send_message(f"Adding {get_steam_url(game_id)} to the wishlist, thanks {interaction.user.mention}!")

    @app_commands.command(name="list", description="list steam games to the wishlist")
    async def lst(self, interaction: Interaction):
        await interaction.response.send_message(f"Here are your steam games on the wishlist: {', '.join(wishlist)}")

    @app_commands.command(name="delete", description="delete a steam games to the wishlist")
    async def delete(self, interaction: Interaction, game_id: str):
        if game_id in wishlist:
            wishlist.remove(game_id)
            handler.info(f"Removing {game_id} from wishlist for user {interaction.user}")
            await interaction.response.send_message(f"Removed {get_steam_url(game_id)} from the wishlist, thanks {interaction.user.mention}!")
        else:
            await interaction.response.send_message(f"steam id not in the list, get fucked {interaction.user.mention}!")