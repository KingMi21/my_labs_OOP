from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...

    @abstractmethod
    def undo(self) -> None:
        ...

    @abstractmethod
    def redo(self) -> None:
        ...


class PrintCharCommand(Command):
    text = ""

    def __init__(self, char: str) -> None:
        self.char = char

    def execute(self) -> str:
        PrintCharCommand.text += self.char
        return PrintCharCommand.text

    def undo(self) -> str:
        PrintCharCommand.text = PrintCharCommand.text[:-1]
        return PrintCharCommand.text

    def redo(self) -> str:
        return self.execute()


class VolumeState:
    _current_volume = 50

    @classmethod
    def get_volume(cls):
        return cls._current_volume

    @classmethod
    def set_volume(cls, value):
        cls._current_volume = max(0, min(100, value))


class VolumeCommand(Command, ABC):
    def __init__(self, amount: int = 20):
        self.amount = amount
        self.previous_volume = None

    def _change_volume(self, change: int) -> str:
        current = VolumeState.get_volume()
        new_volume = current + change
        VolumeState.set_volume(new_volume)
        return new_volume


class VolumeUpCommand(VolumeCommand):
    def execute(self) -> str:
        self.previous_volume = VolumeState.get_volume()
        new_volume = self._change_volume(self.amount)
        return f"громкость увеличена на +{self.amount}% (теперь: {new_volume}%)"

    def undo(self) -> str:
        if self.previous_volume is not None:
            VolumeState.set_volume(self.previous_volume)
            return f"громкость уменьшена на +{self.amount}% (теперь: {self.previous_volume}%)"
        return "Нельзя отменить - нет предыдущего состояния громкости"

    def redo(self) -> str:
        return self.execute()


class VolumeDownCommand(VolumeCommand):
    def execute(self) -> str:
        self.previous_volume = VolumeState.get_volume()
        new_volume = self._change_volume(-self.amount)
        return f"громкость уменьшена на -{self.amount}% (теперь: {new_volume}%)"

    def undo(self) -> str:
        if self.previous_volume is not None:
            VolumeState.set_volume(self.previous_volume)
            return f"громкость увеличена на -{self.amount}% (теперь: {self.previous_volume}%)"
        return "Нельзя отменить - нет предыдущего состояния громкости"

    def redo(self) -> str:
        return self.execute()


class MediaPlayerCommand(Command):
    def __init__(self, is_playing: bool = False) -> None:
        self.is_playing = is_playing

    def execute(self) -> str:
        self.is_playing = True
        return "медиаплеер запущен"

    def undo(self) -> str:
        self.is_playing = False
        return "медиаплеер закрыт"

    def redo(self) -> str:
        return self.execute()
