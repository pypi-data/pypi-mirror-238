from .auth import Auth


class Light:
    """Class that represents a Light object in the ExampleHub API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a light object."""
        self.raw_data = raw_data
        self.auth = auth

    # Note: each property name maps the name in the returned data

    @property
    def id(self) -> int:
        """Return the ID of the light."""
        return self.raw_data["id"]

    @property
    def name(self) -> str:
        """Return the name of the light."""
        return self.raw_data["name"]

    @property
    def is_on(self) -> bool:
        """Return if the light is on."""
        return self.raw_data["id"]

    async def async_control(self, is_on: bool):
        """Control the light."""
        resp = await self.auth.request(
            "post", f"light/{self.id}", json={"is_on": is_on}
        )
        resp.raise_for_status()
        self.raw_data = await resp.json()

    async def async_update(self):
        """Update the light data."""
        resp = await self.auth.request("get", f"light/{self.id}")
        resp.raise_for_status()
        self.raw_data = await resp.json()