import serial
import requests
import json
import datetime


# Function to build and post neoOntology json object and http request
def neoOntJSON(gearID, value):
    # Calculate current dateTime and parse strings
    time = datetime.datetime.now()
    hourString = time.strftime("%y%m%d%H%M%S")
    dateString = time.strftime("%Y-%m-%dT%H:%M:%S")
    # Transform rpm value into hertz and print as string
    valueString = str(float(value) / 60)
    # Determine state, device and component uri according to gearID
    if gearID == 1:
        stateURI = "http://138.250.108.1:3003/api/files/owl/diagont#GB_DrivenShaft_Speed_Frequency_" + hourString
        deviceURI = "http://138.250.108.1:3003/api/files/owl/orgont#GB_DrivenShaft_Overload_Speed"
        componentURI = "http://138.250.108.1:3003/api/files/owl/orgont#1_OpEx-0_1_SHF-W15H6250_1"
        requestURI = "http://138.250.108.1:3003/api/ontologies/diagont/individual/GB_DrivenShaft_Speed_Frequency_" + hourString + "/input"
    elif gearID == 2:
        stateURI = "http://138.250.108.1:3003/api/files/owl/diagont#GB_DrivingShaft_Speed_Frequency_" + hourString
        deviceURI = "http://138.250.108.1:3003/api/files/owl/orgont#GB_DrivingShaft_Overload_Speed"
        componentURI = "http://138.250.108.1:3003/api/files/owl/orgont#1_OpEx-0_1_SHF-W15H6250_1"
        requestURI = "http://138.250.108.1:3003/api/ontologies/diagont/individual/GB_DrivingShaft_Speed_Frequency_" + hourString + "/input"
    else:
        return None
    # Build json object for neoOnt individual input and parse as text string
    requestText = json.dumps({
        "ontName": stateURI,
        "ontOntology": "http://138.250.108.1:3003/api/files/owl/diagont#",
        "ontClass": "http://138.250.108.1:3003/api/files/owl/diagont#State",
        "ontProperties": [
            {
                "ontName": "http://138.250.108.1:3003/api/files/owl/diagont#hasStateValue",
                "ontValue": valueString,
                "ontDomain": "http://138.250.108.1:3003/api/files/owl/diagont#State",
                "ontRange": "http://www.w3.org/2001/XMLSchema#double",
                "ontType": "http://www.w3.org/2002/07/owl#DatatypeProperty"
            },
            {
                "ontName": "http://138.250.108.1:3003/api/files/owl/diagont#hasStateDate",
                "ontValue": dateString,
                "ontDomain": "http://138.250.108.1:3003/api/files/owl/diagont#State",
                "ontRange": "http://www.w3.org/2001/XMLSchema#dateTime",
                "ontType": "http://www.w3.org/2002/07/owl#DatatypeProperty"
            },
            {
                "ontName": "http://138.250.108.1:3003/api/files/owl/diagont#hasStateUnit",
                "ontValue": "http://138.250.108.1:3003/api/files/owl/diagont#hertz",
                "ontDomain": "http://138.250.108.1:3003/api/files/owl/diagont#State",
                "ontRange": "http://138.250.108.1:3003/api/files/owl/diagont#Unit",
                "ontType": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            {
                "ontName": "http://138.250.108.1:3003/api/files/owl/diagont#hasStateStatus",
                "ontValue": "http://138.250.108.1:3003/api/files/owl/diagont#Normal",
                "ontDomain": "http://138.250.108.1:3003/api/files/owl/diagont#State",
                "ontRange": "http://138.250.108.1:3003/api/files/owl/diagont#Status",
                "ontType": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            {
                "ontName": "http://138.250.108.1:3003/api/files/owl/diagont#hasStateDominion",
                "ontValue": "http://138.250.108.1:3003/api/files/owl/diagont#Mechanics",
                "ontDomain": "http://138.250.108.1:3003/api/files/owl/diagont#State",
                "ontRange": "http://138.250.108.1:3003/api/files/owl/diagont#Dominion",
                "ontType": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            {
                "ontName": "http://138.250.108.1:3003/api/files/owl/diagont#hasStatePhenomenon",
                "ontValue": "http://138.250.108.1:3003/api/files/owl/diagont#Overload",
                "ontDomain": "http://138.250.108.1:3003/api/files/owl/diagont#State",
                "ontRange": "http://138.250.108.1:3003/api/files/owl/diagont#Phenomenon",
                "ontType": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            {
                "ontName": "http://138.250.108.1:3003/api/files/owl/diagont#measuredByDevice",
                "ontValue": deviceURI,
                "ontDomain": "http://138.250.108.1:3003/api/files/owl/diagont#State",
                "ontRange": "http://138.250.108.1:3003/api/files/owl/orgont#Device",
                "ontType": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            {
                "ontName": "http://138.250.108.1:3003/api/files/owl/diagont#refersToComponent",
                "ontValue": componentURI,
                "ontDomain": "http://138.250.108.1:3003/api/files/owl/diagont#State",
                "ontRange": "http://138.250.108.1:3003/api/files/owl/orgont#Component",
                "ontType": "http://www.w3.org/2002/07/owl#ObjectProperty"
            }
        ]
    })
    # Send post request to neoOntology server
    requestHeader = {"content-type": "application/json"}
    try:
        requestResult = requests.post(requestURI, data=requestText, headers=requestHeader, timeout=5)
        print(requestResult.content)
        return
    except requests.exceptions.RequestException as e:
        print(e)
        return


# Function to send data over php server
def phpJSON(jsonObject):
    API_ENDPOINT = "http://192.168.43.214:81/LogToDB.php"
    s = json.dumps(jsonObject)
    try:
        requestResult = requests.post(API_ENDPOINT, data=jsonObject, timeout=5)
        print(s)
        print(requestResult.content)
        return
    except requests.exceptions.RequestException as e:
        print(e)
        return


read = serial.Serial('/dev/ttyACM0', 9600)

while True:
    data = read.readline()
    myjson = data.decode('utf8').replace("'", '"')
    j = json.loads(myjson)
    phpJSON(j)
    neoOntJSON(1, j["DrivenGearRPM"])
    neoOntJSON(2, j["DriveGearRPM"])
