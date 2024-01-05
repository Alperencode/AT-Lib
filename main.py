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
    # Set error reporting mode to numeric
    'AT+CMEE=1',

    # Set-up APN (PDP context for GPRS connectivity)
    # 'AT+QICSGP=1,3,"mms","vodafone","vodafone",1',
    'AT+QICSGP=1,1,"UNINET","" ,"" ,1',

    # Configure the HTTP context ID
    'AT+QHTTPCFG="contextid"',

    # Configure the response header for HTTP
    'AT+QHTTPCFG="responseheader",1',

    # Attaches to the GPRS service
    # 'AT+CGATT=1',

    # Activate the PDP context
    # 'AT+QIACT=1',

    # Query the status of the PDP context activation
    'AT+QIACT?',

    # Query the PDP (Packet Data Protocol) context list
    'AT+CGDCONT?',

    # Configure the URL for HTTP operations
    'AT+QHTTPURL=25,80',

    # Set the target URL for HTTP GET request
    # This url will be removed to .env
    'https://webhook.site/85f89f43-b395-426b-be83-cb52c63cd214',

    # HTTP GET request
    'AT+QHTTPGET=80',

    # Activate the SIM Toolkit
    'AT+QSTK=1',

    # Read the HTTP response from the server
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
