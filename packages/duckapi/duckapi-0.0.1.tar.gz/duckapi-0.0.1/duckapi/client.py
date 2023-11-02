from .config import __baseurl__
from .asset import Asset
from .exceptions import NoJSONProperty

from aiohttp import ClientSession
from aiohttp import TCPConnector


async def get_asset(url: str, ssl: bool) -> Asset:
    async with ClientSession(connector=TCPConnector(ssl=ssl)) as session:
        async with session.request(method="GET", url=url, timeout=30) as response:
            if not response.ok:
                response.raise_for_status()

            data = (await response.json()).get("image")

            if data is None:
                raise NoJSONProperty(url=url, json=data, prop="image")

            return Asset(url=data, ssl=ssl)


class DuckAPI:
    def __init__(self, baseurl: str = __baseurl__, ssl: bool = True) -> None:
        self.__baseurl = baseurl
        self.__ssl = ssl

    async def get_asset_from_path(self, path: str) -> Asset:
        return await get_asset(url=self.__baseurl + path, ssl=self.__ssl)

    async def duck(self) -> Asset:
        return await self.get_asset_from_path(path="/duck")

    async def pig(self) -> Asset:
        return await self.get_asset_from_path(path="/pig")

    async def cow(self) -> Asset:
        return await self.get_asset_from_path(path="/cow")

    async def chicken(self) -> Asset:
        return await self.get_asset_from_path(path="/chicken")

    async def cat(self) -> Asset:
        return await self.get_asset_from_path(path="/cat")

    async def dog(self) -> Asset:
        return await self.get_asset_from_path(path="/dog")

    async def goose(self) -> Asset:
        return await self.get_asset_from_path(path="/goose")

    async def turkey(self) -> Asset:
        return await self.get_asset_from_path(path="/turkey")
