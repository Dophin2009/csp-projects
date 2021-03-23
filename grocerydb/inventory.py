from __future__ import annotations

from typing import Dict, List, Optional, Tuple


class _ItemData:
    def __init__(self, price: float, amount: int) -> None:
        self.__price = price
        self.__amount = amount

    def _replace(self, amount: int) -> None:
        self.__amount = amount

    def _restock(self, amount: int):
        self.__amount += amount

    def _remove(self, amount: int):
        if self.__amount < amount:
            raise InsufficientInventoryError(amount, self.__amount)
        else:
            self.__amount -= amount

    @property
    def price(self) -> float:
        return self.__price

    @property
    def amount(self) -> int:
        return self.__amount


class Inventory:
    def __init__(self) -> None:
        self.__items: Dict[str, _ItemData] = {}

    def create(self, name: str,  price: float, amount: int) -> None:
        self.__items[name] = _ItemData(price, amount)

    def delete(self, name: str) -> None:
        del self.__items[name]

    def replace(self, name: str, amount: int) -> None:
        self.__get_item(name)._replace(amount)

    def restock(self, name: str, amount: int) -> None:
        self.__get_item(name)._restock(amount)

    def remove(self, name: str, amount: int) -> None:
        self.__get_item(name)._remove(amount)

    def get(self, name: str) -> Optional[Tuple[float, int]]:
        if name in self.__items.keys():
            data = self.__items[name]
            return (data.price, data.amount)
        else:
            return None

    def items(self) -> List[Tuple[str, float, int]]:
        return [(name, data.price, data.amount)
                for name, data in self.__items.items()]

    def __get_item(self, name: str) -> _ItemData:
        if name in self.__items.keys():
            return self.__items[name]
        else:
            raise ItemNotFoundError(name)


class ItemNotFoundError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name
        self.message = 'Item with name {} not found'.format(self.name)
        super().__init__(self.message)


class InsufficientInventoryError(Exception):
    def __init__(self, diff: int, total: int) -> None:
        self.diff = diff
        self.total = total
        self.message = ('Cannot remove {} stock from inventory with '
                        '{} items').format(self.diff, self.total)
        super().__init__(self.message)
