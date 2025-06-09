from typing import Optional
import json
from commands import *
from memento import KeyboardMemento


class VirtualKeyboard:
    def __init__(self) -> None:
        self.key_bindings: dict[str, Command] = {}
        self.history: list[dict[str, Command]] = []
        self.undo_stack: list[dict[str, Command]] = []

        self.init_default_bindings()

    def init_default_bindings(self) -> None:
        self.bind_key("a", PrintCharCommand("a"))
        self.bind_key("b", PrintCharCommand("b"))
        self.bind_key("c", PrintCharCommand("c"))
        self.bind_key("d", PrintCharCommand("d"))
        self.bind_key("ctrl++", VolumeUpCommand())
        self.bind_key("ctrl+-", VolumeDownCommand())
        self.bind_key("ctrl+p", MediaPlayerCommand())
        self.bind_key("undo", None)
        self.bind_key("redo", None)

    def bind_key(self, key: str, command: Optional[Command]) -> None:
        self.key_bindings[key] = command

    def press_key(self, key: str) -> str | None:
        if key == "undo":
            return self.undo()
        elif key == "redo":
            return self.redo()

        command = self.key_bindings.get(key)
        if not command and len(key) == 1:
            self.bind_key(key, PrintCharCommand(key))
            command = self.key_bindings.get(key)
        if command:
            result = command.execute()
            self.history.append({"key": key, "command": command})
            self.undo_stack.clear()
            return result
        return f"Неизвестная клавиша: {key}"

    def undo(self) -> str:
        if not self.history:
            return "Нечего отменять"

        command = self.history.pop()
        result = command["command"].undo()
        self.undo_stack.append(command)
        return f"отмена: {result}"

    def redo(self) -> str:
        if not self.undo_stack:
            return "Нечего повторить"

        command = self.undo_stack.pop()
        result = command["command"].redo()
        self.history.append(command)
        return f"повтор: {result}"

    def save_state(self, filename: str = "data/keyboard_state.json") -> None:
        memento = KeyboardMemento.from_keyboard(self)
        try:
            with open(filename, "w") as f:
                json.dump(memento.state, f, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения состояния: {e}")
            raise e

    def load_state(self, filename: str = "data/keyboard_state.json") -> bool:
        try:
            with open(filename, "r") as f:
                state = json.load(f)

            PrintCharCommand.text = state['text']
            VolumeState.set_volume(state.get('volume', 50))

            self.key_bindings.clear()
            for key, command_data in state.get('key_bindings', {}).items():
                if command_data is None:
                    self.key_bindings[key] = None
                else:
                    command_class = globals()[command_data['class']]
                    if command_data['class'] in ('VolumeUpCommand', 'VolumeDownCommand'):
                        command = command_class(command_data['state'].get('amount', 20))
                    elif command_data['class'] == 'MediaPlayerCommand':
                        command = command_class(command_data['state'].get('is_playing', False))
                    elif command_data['class'] == 'PrintCharCommand':
                        command = command_class(command_data['state'].get('char', ''))
                    else:
                        command = command_class(**command_data['state'])
                    self.key_bindings[key] = command

            self.history = [
                {"key": key, "command": self.key_bindings[key]}
                for key in state.get('history', [])
                if key in self.key_bindings.keys() and self.key_bindings[key] is not None
            ]

            self.undo_stack = [
                {"key": key, "command": self.key_bindings[key]}
                for key in state.get('undo_stack', [])
                if key in self.key_bindings.keys() and self.key_bindings[key] is not None
            ]
            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError, AttributeError) as e:
            print(f"Ошибка загрузки состояния: {e}")
            return False
