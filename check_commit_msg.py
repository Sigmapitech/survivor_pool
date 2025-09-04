#!/usr/bin/env python3
import os
import pathlib
import sys


def has_correct_message(msg: str) -> bool:
    print(f"Commit message:\n{msg}")

    if msg == "!":
        return True

    verb, *words = msg.split()
    report = {
        "  " in msg: "double space!",
        msg.startswith(" ") or msg.endswith(" "): "leading or trailling space",
        not verb[0].isalpha(): "first caracter must be a letter",
        verb[0].islower(): "verb is not capitalized",
        any(map(verb.endswith, {"ed", "ing", "s"})): "use imperative tense",
        msg.endswith("."): "message should not end with a period",
        len(words) < 2: "include at least 3 words",
    }.get(True)

    if report is None:
        return True

    print(report)
    return False


def main():
    if len(sys.argv) != 2:
        return os.EX_USAGE

    message = pathlib.Path(sys.argv[1]).read_text()
    first_line = message.splitlines()[0]
    return not has_correct_message(first_line)


if __name__ == "__main__":
    sys.exit(main())
