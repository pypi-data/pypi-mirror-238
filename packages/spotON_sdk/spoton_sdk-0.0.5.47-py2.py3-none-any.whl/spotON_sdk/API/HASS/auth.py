from aiohttp import ClientSession, ClientResponse


class Auth:
    """Class to make authenticated requests."""

    def __init__(self, websession: ClientSession, host: str, access_token: str):
        """Initialize the auth."""
        self.websession = websession
        self.host = host
        self.access_token = access_token

    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)
        
        headers = {'Content-type': 'application/json'} # Set the content type to JSON
        #headers["authorization"] = self.access_token
        print (f"{path}")
        return await self.websession.request(
            method, f"{self.host}/{path}", **kwargs, headers=headers,
        )
    
import asyncio
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://km28t5snp5.execute-api.eu-central-1.amazonaws.com/Prod/echo'
        url = 'http://127.0.0.1:8000'

        auth = Auth(session, url, "secret_access_token")

        # This will fetch data from http://example.com/api/lights
        resp = await auth.request("get", "lights")
        print("HTTP response status code", resp.status)
        print("HTTP response JSON content", await resp.json())



asyncio.run(main())