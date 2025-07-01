import sys
import os

DEFAULT_EXE = "alembic"
OTHER_EXE = {
    "hist": os.path.expanduser("~/alemhist/alemhist"),
    "rebase": os.path.expanduser("~/alemhist/rebase"),
    "reindex": os.path.expanduser("~/alemhist/reindex"),
}
ALIASES = {
    "b": "branches",
    "branch": "branches",
    "c": "current",
    "cur": "current",
    "d": "downgrade",
    "do": "downgrade",
    "down": "downgrade",
    "e": "edit",
    "head": "heads",
    "h": "hist",
    "i": "init",
    "lt": "list_templates",
    "m": "merge",
    "r": "revision",
    "rev": "revision",
    "u": "upgrade",
    "up": "upgrade",
}
DEFAULT_PARAMS = {
    "downgrade": ["-1"],
    "upgrade": ["head"],
    "merge": ["heads"],
}


def ale(argv):
    if len(argv) == 0:
        return DEFAULT_EXE

    command = argv[0]
    params = argv[1:]
    if command in ALIASES:
        command = ALIASES[command]
    if len(params) == 0 and command in DEFAULT_PARAMS:
        params = DEFAULT_PARAMS[command]
    params = [repr(param) if " " in param else param for param in params]
    if command in OTHER_EXE:
        return " ".join([OTHER_EXE[command]] + params)
    return " ".join([DEFAULT_EXE, command] + params)


print(ale(sys.argv[1:]))
