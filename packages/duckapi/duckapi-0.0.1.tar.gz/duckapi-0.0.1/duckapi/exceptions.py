class NoJSONProperty(Exception):
    def __init__(self, url: str, json: object, prop: str) -> None:
        self.__url = url
        self.__json = json
        self.__prop = prop
    
    @property
    def url(self) -> str:
        return self.__url

    @property
    def json(self) -> str:
        return self.__json
    
    def __repr__(self) -> str:
        return "no property named '%s' found in JSON" % self.__prop
