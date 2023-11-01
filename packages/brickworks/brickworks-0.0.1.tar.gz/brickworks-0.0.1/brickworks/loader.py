import importlib

from brickworks.settings import BrickworksSettings


def load_modules(settings: BrickworksSettings) -> None:
    for module in settings.bricks:
        importlib.import_module(module)
