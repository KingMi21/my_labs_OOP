from typing import Self
from commands import PrintCharCommand, VolumeState, VolumeUpCommand, VolumeDownCommand, MediaPlayerCommand


class KeyboardMemento:
    def __init__(self, state: dict) -> None:
        self.state = state

    @classmethod
    def from_keyboard(cls, keyboard) -> Self:
        text = PrintCharCommand.text
        volume = VolumeState.get_volume()

        key_bindings = {}
        for key, command in keyboard.key_bindings.items():
            if command is None:
                key_bindings[key] = None
            else:
                command_data = {
                    'class': command.__class__.__name__,
                    'state': {}
                }

                # Сохраняем только необходимые атрибуты
                if isinstance(command, (VolumeUpCommand, VolumeDownCommand)):
                    command_data['state']['amount'] = command.amount
                elif isinstance(command, MediaPlayerCommand):
                    command_data['state']['is_playing'] = command.is_playing
                elif isinstance(command, PrintCharCommand):
                    command_data['state']['char'] = command.char

                key_bindings[key] = command_data

        return cls({
            'text': text,
            'volume': volume,
            'key_bindings': key_bindings,
            'history': [command["key"] for command in keyboard.history],
            'undo_stack': [command["key"] for command in keyboard.undo_stack]
        })