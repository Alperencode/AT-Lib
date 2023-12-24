from source.atlib import ATLIB


if __name__ == "__main__":
    atlib = ATLIB(ATLIB.get_port())

    commands = [
        "AT",
        "ATI",
        "AT*NOKIATEST",
        "AT+CMD",
        "",
        "AT+CSQ",
    ]

    for command in commands:
        print(atlib.send_and_get(command))
