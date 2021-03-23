from typing import Optional

from .inventory import Inventory


class InventoryLoader:
    def __init__(self, inventory: Inventory, filepath: str) -> None:
        self.__inventory = inventory
        self.__filepath = filepath

    def load(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = self.__filepath

        try:
            with open(filepath, 'r') as f:
                lines = f.read().splitlines()

            for line in lines:
                data = line.split('\t')
                name = data[0]
                price = float(data[1])
                stock = int(data[2])
                self.__inventory.create(name, price, stock)
        except IOError:
            with open(filepath, 'w'):
                pass

    def save(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = self.__filepath

        lines = ['{}\t{}\t{}\n'.format(name, price, stock)
                 for name, price, stock in self.__inventory.items()]

        with open(filepath, 'w') as f:
            f.writelines(lines)
