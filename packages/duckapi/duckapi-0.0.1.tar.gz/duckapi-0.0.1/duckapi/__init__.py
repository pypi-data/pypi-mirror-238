# wrapper developed by Its-MatriX | https://github.com/Its-MatriX/duckapi-wrapper
# API developed by Lcvb-X         | https://github.com/Lcvb-x/DuckApi


from .config import __version__
from .config import __baseurl__

from .asset import Asset

from .client import DuckAPI
from .client import get_asset

from .exceptions import NoJSONProperty
