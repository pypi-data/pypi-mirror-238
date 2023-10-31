from typing import List

from .auth import Auth
from .light import Light


class ExampleHubAPI:
    """Class to communicate with the ExampleHub API."""

    def __init__(self, auth: Auth):
        """Initialize the API and store the auth so we can make requests."""
        self.auth = auth

    async def async_get_lights(self) -> List[Light]:
        """Return the lights."""
        resp = await self.auth.request("get", "lights")
        resp.raise_for_status()
        return [Light(light_data, self.auth) for light_data in await resp.json()]

    async def async_get_light(self, light_id) -> Light:
        """Return the lights."""
        resp = await self.auth.request("get", f"light/{light_id}")
        resp.raise_for_status()
        return Light(await resp.json(), self.auth)

