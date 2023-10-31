import json
from importlib import resources

import auto_phylo
from auto_phylo.pipeliner.model.Command import Command
from auto_phylo.pipeliner.model.Commands import Commands


def load_commands() -> Commands:
    with resources.open_text(auto_phylo, "commands.json", "utf-8") as file:
        commands = json.load(file)

    return Commands(Command(**data) for data in commands)
