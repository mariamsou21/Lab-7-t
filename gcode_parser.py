"""G-Code parser for the SED1115 pen plotter (Lab 7).

Pure Python (no hardware imports) so it can be unit tested on a laptop.

A parsed command is a dict:
    {"command": "G1", "params": {"S": 47.847, "E": 57.273}}
"""


def parse_line(line):
    """Parse one line of G-Code.

    Returns a command dict, or None for blank lines / comments.
    Raises ValueError if a parameter value is not a number.
    """
    # Remove anything after a ';' comment marker, then surrounding whitespace
    line = line.split(";")[0].strip()
    if not line:
        return None

    words = line.split()
    command = words[0].upper()

    params = {}
    for word in words[1:]:
        letter = word[0].upper()
        params[letter] = float(word[1:])  # e.g. "S47.847" -> 47.847

    return {"command": command, "params": params}


def parse_file(filename):
    """Read a G-Code file and return a list of command dicts."""
    commands = []
    with open(filename, "r") as f:
        for line in f:
            cmd = parse_line(line)
            if cmd is not None:
                commands.append(cmd)
    return commands
