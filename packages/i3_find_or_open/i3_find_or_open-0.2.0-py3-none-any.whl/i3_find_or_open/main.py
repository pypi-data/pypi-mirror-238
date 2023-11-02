"""A module that helps you bind keys to find and display, or open a window in i3wm."""
#!/bin/python
import argparse
import json
import re
import subprocess as sp

import flatdict


def find_window(tree: dict, title: str) -> int | None:
    """Finds a window by title regex in an i3 tree.

    Args:
        tree (dict): A tree as found by `i3-msg -t get_tree`.
        title (str): A regex that describes the title of the window you are trying to
            find.

    Returns:
        window (int): The workspace the window has been found on. None if it doesn't
            exist.

    """
    pass
    for workspace in tree:
        ws = flatdict.FlatterDict(workspace)
        if len(
            list(
                filter(  # type: ignore
                    re.compile(title).match,  # type: ignore
                    [
                        ws[x]
                        for x in filter(re.compile(".*name$").match, ws.keys())
                        if ws[x] is not None
                    ],
                )
            )
        ):
            return ws["name"]  # type: ignore
    return None


def main():
    """Main function for binary."""
    # parse arguments
    parser = argparse.ArgumentParser(
        prog="i3-find-or-open",
        description="A command-line utility that helps you bind keys to find and display a window, or open it if there is no instance running in i3wm.",  # noqa: E501
    )
    parser.add_argument(
        "title",
        type=str,
        help="A regex that will match the window title that you are trying to find.",
    )
    parser.add_argument(
        "command",
        type=str,
        help="The command that will be run if the window is not open.",
    )
    args = parser.parse_args()

    tree = json.loads(sp.run(["i3-msg", "-t", "get_tree"], capture_output=True).stdout)
    if len(
        list(
            filter(
                re.compile(args.title).match,
                [
                    x["nodes"][0]["name"]
                    for x in tree["nodes"][0]["nodes"][0]["nodes"][0]["floating_nodes"]
                ],
            )
        )
    ):
        sp.run(
            f"i3-msg '[title=\"{args.title}\"] scratchpad show'",
            shell=True,
        )
    else:
        output = 1
        ws = None
        while ws is None and output < len(tree["nodes"]):
            ws = find_window(tree["nodes"][output]["nodes"][1]["nodes"], args.title)
            output += 1
        if ws is not None:
            sp.run(f"i3-msg 'workspace {ws}' &> /dev/null", shell=True)
        else:
            sp.run(args.command, shell=True)
