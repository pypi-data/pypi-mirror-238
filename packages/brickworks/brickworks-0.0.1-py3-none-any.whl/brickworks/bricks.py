import importlib
import json
import os
from dataclasses import dataclass

from brickworks.settings import BrickworksSettings


def get_bricks(settings: BrickworksSettings):
    """
    Load all bricks from the settings
    """
    bricks = []
    for brick in settings.bricks:
        bricks_json_path = _get_bricks_json_path(brick)
        with open(bricks_json_path, "r", encoding="UTF-8") as f:
            bricks_json = json.load(f)
            bricks.append(Brick(path=brick, routers=bricks_json.get("routers", [])))

    return bricks


def _get_bricks_json_path(module_name):
    # Get the path to the directory where the module is located
    module = importlib.import_module(module_name)
    module_dir = os.path.dirname(str(module.__file__))

    # Construct the path to the "bricks.json" file
    bricks_json_path = os.path.join(module_dir, "brick.json")

    return bricks_json_path


@dataclass
class Brick:
    path: str
    routers: list[str]
