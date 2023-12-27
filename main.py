from source.atlib import ATLIB


test_commands = [
    "AT",
    "ATI",
    "AT*NOKIATEST",
    "AT+CMD",
    "",
    "AT+CSQ",
    "RANDOMMESSAGE"
]

report_commands = [
    'AT+CMEE=2',    # Error reporting mode
    'AT+CSQ',       # Signal Quality Report
    'AT+CGDCONT?',  # Query PDP Context List
    'AT+CREG?',     # Network Registration Status / +CREG: 0,5: registered
    'AT+CPIN?',     # Query SIM Card Status
    'AT+CGATT?',    # GPRS Attachment Status / +CGATT: 1: GPRS attached
    'AT+CEER',      # Extended Error Report
    'AT+HTTPINIT',  # Initialize HTTP Service
]

request_commands = [
    'AT+HTTPCLIENT=1,0,"http://httpbin.org/get","httpbin.org","/get",1',
]

if __name__ == "__main__":
    at = ATLIB(ATLIB.get_port())

    for command in report_commands:
        print(at.send_and_get(command))
