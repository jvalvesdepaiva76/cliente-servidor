# File: server/data_structures/hash_map.py

class HashMap:
    def __init__(self, size=100):
        self.size = size
        self.map = [None] * size

    def _hash(self, key):
        return hash(key) % self.size

    # Placeholder for HashMap operations: add, remove, and get.
    def add(self, key, value):
        pass

    def remove(self, key):
        pass

    def get(self, key):
        pass
