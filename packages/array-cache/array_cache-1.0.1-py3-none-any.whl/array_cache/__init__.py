""" array_cache package """
from json import loads, dumps
from os.path import expanduser
from os.path import exists
from hashlib import sha256


class ArrayCache:
    """caching a file"""

    CACHE_FILE = f"{expanduser('~')}/.python_lib_cache_word"

    def __init__(self, data, identifier, cache_delay=5):
        self.hashed = sha256(f"{identifier}".encode("utf-8")).hexdigest()
        self.cache_delay = cache_delay
        self.file = data
        self.cache_index = []
        self.load_cache()

    def load_cache(self):
        """load the cached file"""
        if not exists(self.CACHE_FILE):
            self.save_cache()
        cache = self.safe_load_cache()
        if self.hashed in cache:
            self.cache_index = cache[self.hashed]
        else:
            self.cache_index = 0
            self.save_cache()

    def safe_load_cache(self):
        """load the cached file"""
        with open(self.CACHE_FILE, "r", encoding="utf-8") as reading_file:
            try:
                return loads(reading_file.read())
            except:
                return {}

    def save_cache(self):
        """save the cached file"""
        if not exists(self.CACHE_FILE):
            self.write_cache({})
        cache = self.safe_load_cache()
        cache[self.hashed] = self.cache_index
        self.write_cache(cache)

    def write_cache(self, new_cache):
        """write cache"""
        with open(self.CACHE_FILE, "w", encoding="utf-8") as wrinting_file:
            wrinting_file.write(dumps(new_cache))

    def get_data(self):
        """get an element from the file"""
        index_file = self.cache_index
        while self.file[index_file]:
            yield self.file[index_file]
            index_file = index_file + 1
            if index_file % self.cache_delay == 0:
                self.cache_index = index_file
                self.save_cache()
