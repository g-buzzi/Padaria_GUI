from abc import ABC, abstractmethod
import pickle

class DAO(ABC):
    @abstractmethod
    def __init__(self, datasource="") -> None:
        super().__init__()
        self.__datasource = datasource
        self._cache = {}
        try:
            self._load()
        except (FileNotFoundError, EOFError):
            self._dump()
    
    def _dump(self):
        pickle.dump(self._cache, open(self.__datasource, "wb"))

    def _load(self):
        self._cache = pickle.load(open(self.__datasource, "rb"))

    @abstractmethod
    def get(self, key):
        try:
            return self._cache[key]
        except KeyError:
            raise KeyError

    @abstractmethod
    def add(self, key, obj):
        self._cache[key] = obj
        self._dump()

    @abstractmethod
    def remove(self, key):
        try:
            self._cache.pop(key)
            self._dump()
        except KeyError:
            raise KeyError

#    @abstractmethod
    def alter(self, old_key, new_key, obj):
        try:
            self._cache.pop(old_key)
            self._cache[new_key] = obj
            self._dump()
        except KeyError:
            raise KeyError
    
    def get_all(self):
        return self._cache

    def get_objects(self):
        return self._cache.values()

    def get_keys(self):
        return self._cache.keys()

