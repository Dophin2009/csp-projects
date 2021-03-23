from __future__ import annotations

import re
import sys
from typing import List, Optional

from grocerydb import Inventory, InventoryLoader


def main() -> None:
    args = sys.argv[1:]

    args_c = len(args)
    if args_c == 0:
        dbpath = None
    elif args_c == 1:
        dbpath = args[0]
    else:
        print('Unexpected arguments: expected <=1, found {}'.format(args_c))
        sys.exit(2)

    gdb = GroceryDB()
    gdb.load_inventory(dbpath)

    while True:
        print('> ', end='')
        exit = gdb.prompt()
        if exit:
            break

    gdb.save_inventory(dbpath)


class GroceryDB:
    def __init__(self, dbpath: str = 'inventory.txt') -> None:
        self.__inventory = Inventory()
        self.__loader = InventoryLoader(self.__inventory, dbpath)

    def prompt(self) -> bool:
        query = input()
        if query == '':
            return False

        parts = re.split(' +', query)
        parts = [s for s in parts if len(s) > 0]
        cmd = parts[0]
        args = parts[1:]

        if cmd == 'help':
            return self.help_cmd(args)
        elif cmd == 'ls':
            return self.ls_cmd(args)
        elif cmd == 'add':
            return self.add_cmd(args)
        elif cmd == 'restock':
            return self.restock_cmd(args)
        elif cmd == 'buy':
            return self.buy_cmd(args)
        elif cmd == 'load':
            return self.load_cmd(args)
        elif cmd == 'save':
            return self.save_cmd(args)
        elif cmd == 'exit' or cmd == 'quit':
            return self.exit_cmd(args)
        else:
            return self.unknown_cmd(cmd)

    def help_cmd(self, args: List[str]) -> bool:
        if len(args) > 0:
            print('help expected 0 args')
        else:
            help_str = '''GroceryDB help

    help        Show help information
    ls          Print current inventory
    add         Create a new item or update an existing item
    restock     Add to the stock of an existing item
    buy         Remove from the stock of an existing item
    load        Load the inventory from a file
    save        Save the inventory to a file
    exit        Exit GroceryDB
'''
            print(help_str)

        return False

    def ls_cmd(self, args: List[str]) -> bool:
        if len(args) < 1:
            searchterm = None
        elif len(args) > 1:
            print('ls expected <= 1 args: [searchterm]')
            return False
        else:
            searchterm = args[0]

        self.show_inventory(searchterm)
        return False

    def add_cmd(self, args: List[str]) -> bool:
        help_str = 'add expected 3 args: <name> <price> <stock>'
        if len(args) < 3:
            print(help_str)
        elif len(args) > 3:
            print(help_str)
        else:
            name = args[0]
            price = float(args[1])
            stock = int(args[2])
            self.add_item(name, price, stock)

        return False

    def restock_cmd(self, args: List[str]) -> bool:
        help_str = 'restock expected 2 args: <name> <stock>'
        if len(args) < 2:
            print(help_str)
        elif len(args) > 2:
            print(help_str)
        else:
            name = args[0]
            amount = int(args[1])
            self.restock_item(name, amount)

        return False

    def buy_cmd(self, args: List[str]) -> bool:
        help_str = 'buy expected 2 args: <name> <amount>'
        if len(args) < 2:
            print(help_str)
        elif len(args) > 2:
            print(help_str)
        else:
            name = args[0]
            amount = int(args[1])
            self.buy_item(name, amount)

        return False

    def load_cmd(self, args: List[str]) -> bool:
        if len(args) < 1:
            filepath = None
        elif len(args) > 1:
            print('load expected <=1 args: [filepath]')
            return False
        else:
            filepath = args[0]

        self.load_inventory(filepath)
        return False

    def save_cmd(self, args: List[str]) -> bool:
        if len(args) < 1:
            filepath = None
        elif len(args) > 1:
            print('save expected <=1 args: [filepath]')
            return False
        else:
            filepath = args[0]

        self.__loader.save(filepath)
        return False

    def exit_cmd(self, args: List[str]) -> bool:
        if len(args) > 0:
            print('exit expected 0 args')
        return True

    def unknown_cmd(self, cmd: str) -> bool:
        print('{} not found'.format(cmd))
        return False

    def show_inventory(self, searchterm: Optional[str]) -> None:
        format_row = '{:<12}' * 3
        print(format_row.format('Name', 'Price', 'Stock'))

        items = self.__inventory.items()
        if searchterm is not None:
            items = [data for data in items if searchterm in data[0]]

        for name, price, stock in items:
            print(format_row.format(name, price, stock))

    def add_item(self, name: str, price: float, stock: int) -> None:
        self.__inventory.create(name, price, stock)

    def restock_item(self, name: str, amount: int) -> None:
        self.__inventory.restock(name, amount)

    def buy_item(self, name: str, amount: int) -> None:
        self.__inventory.remove(name, amount)

    def load_inventory(self, filepath: Optional[str] = None) -> None:
        self.__loader.load(filepath)

    def save_inventory(self, filepath: Optional[str] = None) -> None:
        self.__loader.save(filepath)


if __name__ == '__main__':
    main()
