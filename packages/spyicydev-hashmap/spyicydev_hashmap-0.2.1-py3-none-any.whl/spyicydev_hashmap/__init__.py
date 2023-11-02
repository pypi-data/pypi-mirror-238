from typing import Optional, Any


class HashMap:
    def __init__(self, _size: int = 100):
        self.size: int = _size
        self.map_list: list[Optional[list[Any]]] = [None] * self.size

    def _get_hash(self, key: Any) -> int:
        return hash(key) % self.size

    def add(self, key: Any, value: Any) -> None:
        index = self._get_hash(key)
        key_value = [key, value]

        if self.map_list[index] is None:
            self.map_list[index] = [key_value]
        else:
            for pair in self.map_list[index]:
                if pair[0] == key:
                    pair[1] = value
                    return None
                self.map_list[index].append(key_value)

    def get(self, key: Any) -> Optional[Any]:
        index = self._get_hash(key)

        if self.map_list[index] is not None:
            for pair in self.map_list[index]:
                if pair[0] == key:
                    return pair[1]
        return None

    def remove(self, key: Any) -> None:
        index = self._get_hash(key)

        if self.map_list[index] is not None:
            for i, pairs in enumerate(self.map_list[index]):
                if pairs[0] == key:
                    self.map_list[index].pop(i)
                    return None

    def count(self) -> int:
        count: int = 0
        for i in self.map_list:
            if i is not None:
                for j in i:
                    count += 1
        return count

    def get_keys(self) -> list[Any]:
        keys = []
        for i in self.map_list:
            if i is not None:
                for j in i:
                    keys.append(j[0])
        return keys

    def get_pairs(self) -> list[Any]:
        pairs = []
        for i in self.map_list:
            if i is not None:
                for j in i:
                    pairs.append(j)
        return pairs
