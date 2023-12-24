from source.atlib import ATLIB


if __name__ == "__main__":
    at = ATLIB(ATLIB.get_port())

    commands = [
        "AT",
        "ATI",
        "AT*NOKIATEST",
        "AT+CMD",
        "",
        "AT+CSQ",
        "RANDOMMESSAGE"
    ]

    for command in commands:
        print(at.send_and_get(command))
