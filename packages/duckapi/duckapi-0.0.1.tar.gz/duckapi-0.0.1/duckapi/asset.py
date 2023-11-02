from aiohttp import ClientSession
from aiohttp import TCPConnector

from requests import request


class Asset:
    def __init__(self, url: str, ssl: bool) -> None:
        self.__url = url
        self.__ssl = ssl

    @property
    def url(self) -> str:
        return self.__url

    async def download(self) -> bytes:
        async with ClientSession(connector=TCPConnector(ssl=self.__ssl)) as session:
            async with session.request(
                method="GET", url=self.__url, timeout=30
            ) as response:
                if not response.ok:
                    response.raise_for_status()

                return await response.content.read()

    def sync_download(self) -> bytes:
        response = request(method="GET", url=self.__url, verify=self.__ssl)

        if not response.ok:
            response.raise_for_status()

        return response.content
