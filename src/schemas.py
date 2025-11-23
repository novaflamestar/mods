from pydantic import BaseModel


class SteamAppGame(BaseModel):
    app_id: int
    name: str

    def __str__(self):
        return f"{self.name} (App ID: {self.app_id})"
