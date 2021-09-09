from abc import ABC, abstractmethod
import pickle

class DAO(ABC):
    @abstractmethod
    def __init__(self, datasource="") -> None:
        super().__init__()
        self.__datasource = datasource
        self.__cache = {}
        try:
            self.__load()
        except (FileNotFoundError, EOFError):
            self.__dump()
    
    def __dump(self):
        pickle.dump(self.__cache, open(self.__datasource, "wb"))

    def __load(self):
        self.__cache = pickle.load(open(self.__datasource, "rb"))

    @abstractmethod
    def get(self, key):
        try:
            return self.__cache[key]
        except KeyError:
            raise KeyError

    @abstractmethod
    def add(self, key, obj):
        self.__cache[key] = obj
        self.__dump()

    @abstractmethod
    def remove(self, key):
        try:
            self.__cache.pop(key)
            self.__dump()
        except KeyError:
            raise KeyError
    
    def get_all(self):
        return self.__cache

    def get_objects(self):
        return self.__cache.values()

    def get_keys(self):
        return self.__cache.keys()

