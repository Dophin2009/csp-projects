import sys
from typing import List

from PySide2 import QtCore  # type: ignore
from PySide2 import QtGui
from PySide2 import QtQml
from PySide2 import QtQuick
from PySide2 import QtWidgets

import game
from game import GameState
from game import Pile


class PileWrapper(QtCore.QObject):
    def __init__(self, pile: Pile):
        self.__pile = pile

    def _sticks(self):
        return self.__pile.sticks

    sticks = QtCore.Property(int, _sticks, notify=QtCore.Signal())


class PilesListWrapper(QtCore.QAbstractListModel):

    def __init__(self, piles: List[PileWrapper]):
        super(PilesListWrapper, self).__init__()
        self.__piles = piles

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__piles)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.listdata[index.row()])
        else:
            return QtCore.QVariant()


class StateWrapper(QtCore.QObject):
    """
    GameState wrapper that emits a signal when the internal state value is
    updated.
    """

    "Signal that indicates the state has been updated."
    updated = QtCore.Signal()

    def __init__(self, state: GameState):
        super(StateWrapper, self).__init__()
        self.__state = state

    @classmethod
    def empty(cls):
        return cls(None)

    def update(self, state: GameState):
        "Replace the internal state value and emit updated signal."
        self.__state = state
        self.updated.emit()

    def _status_text(self) -> str:
        if self.__state is None or self.__state.current_player < 0:
            return "Waiting..."
        return "Player {}'s turn...".format(self.__state.current_player)

    status_text = QtCore.Property(str, _status_text, notify=updated)

    def _current_player(self):
        return self.__state.current_player

    "Property to retrieve the number of the current player."
    current_player = QtCore.Property(
        int, _current_player, notify=updated)

    def _player_count(self):
        return self.__state.player_count

    "Property to retrieve the total number of players."
    player_count = QtCore.Property(int, _player_count, notify=updated)

    def _piles(self):
        print("fawjkflwaj")
        return PilesListWrapper([PileWrapper(p) for p in self.__state.piles])

    # How the heck do list properties work?
    piles = QtCore.Property(QtQml.QQmlListReference, _piles, notify=updated)

    def _clear(self):
        return self.__state.clear()

    "Property to retrieve the clear state of the board."
    clear = QtCore.Property(bool, _clear, notify=updated)


class Interface(game.Interface):
    def __init__(self):
        # Store state wrapper to later update.
        self.state_obj = StateWrapper.empty()

    def update(self, state: GameState):
        # When game logic calls this, the state value is updated and the
        # updated signal is emitted.
        self.state_obj.update(state)
        print(state.__dict__)

    def prompt_pile(self, state: GameState) -> int:
        return int(input("pile?"))

    def prompt_take(self, pile: Pile) -> int:
        return int(input("take?"))

    def game_over(self, state: GameState):
        pass


class Game(game.Game):
    def __init__(self, interface: Interface):
        game.Game.__init__(self, interface, 2, 2)

        self.interface.update(self.state)


class GameThread(QtCore.QThread):
    def __init__(self, game: Game):
        super(GameThread, self).__init__()
        self.game = game

    def run(self):
        self.game.loop()


def application(args: List[str]):
    interface = Interface()
    game_instance = Game(interface)
    game_thread = GameThread(game_instance)

    app = QtWidgets.QApplication(args)
    view = QtQuick.QQuickView()

    rc = view.rootContext()
    rc.setContextProperty('gameState', interface.state_obj)

    view.setSource(QtCore.QUrl("gui.qml"))
    view.show()

    game_thread.start()

    ret = app.exec_()
    game_thread.exit()
    return ret


if __name__ == "__main__":
    sys.exit(application(sys.argv))
