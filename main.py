from source.atlib import ATLIB
import sys


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
    # 'AT+QICSGP=1,3,"mms","vodafone","vodafone",1',
    'AT+CMEE=1',
    'AT+QHTTPCFG="contextid"',
    'AT+QHTTPCFG="responseheader",1',
    'AT+QICSGP=1,1,"UNINET","" ,"" ,1',
    'AT+CGATT=1',
    # 'AT+QIACT=1',
    # 'AT+QIACT?',
    'AT+CGDCONT?',
    'AT+QHTTPURL=25,80',
    'https://webhook.site/85f89f43-b395-426b-be83-cb52c63cd214',
    'AT+QHTTPGET=80',
    'AT+QSTK=1',
    'AT+QHTTPREAD=80'
]

if __name__ == "__main__":
    at = ATLIB(ATLIB.get_port())

    sys.argv.pop(0)
    if sys.argv:
        for command in sys.argv:
            print(at.send_and_get(str(command)))
    else:
        for command in request_commands:
            print(at.send_and_get(command))
