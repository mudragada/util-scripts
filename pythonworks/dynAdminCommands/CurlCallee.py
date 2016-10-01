__author__ = 'Krishna Mudragada'

import re, requests, scp, paramiko, socket, logging, os, shutil, sys
from requests import exceptions
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from Constants import HTTPConstants
from Constants import DynAdminConstants

class CurlCallee:
    constants = DynAdminConstants()
    httpConstants = HTTPConstants()
    logging.basicConfig(format='%(asctime)s %(message)s')
    logging.getLogger().setLevel(logging.INFO)

    def copyInstancesFileToLocal(self):
        if(socket.gethostname().startswith(self.constants.statsHost)):
            logging.info("You're already on " + self.constants.statsHost +", skipping the scp and doing a cp")
            shutil.copyfile(self.constants.instancesFileLocation + self.constants.instancesFile, self.constants.instancesFile)
        else:
            logging.info("SCP'ing the " + self.constants.instancesFile + " from " + self.constants.statsHost + ":" + self.constants.instancesFileLocation)
            sshClient = paramiko.SSHClient()
            sshClient.load_system_host_keys()
            sshClient.connect(self.constants.statsHost)
            scpClient = scp.SCPClient(sshClient.get_transport())
            scpClient.get(self.constants.instancesFileLocation + self.constants.instancesFile)
            scpClient.close()
            sshClient.close()
            logging.info("SCPing " + self.constants.instancesFile + " to " + socket.gethostname() + " is COMPLETE")


    def checkInstancesFile(self):
        if(not os.path.isfile(self.constants.instancesFile)):
            logging.error("Instances file not found. Pls check.")
            sys.exit()
        if (os.stat(self.constants.instancesFile).st_size == 0):
            logging.error("Instances file is empty. Pls check")
            sys.exit()



    def curlOnFirstSocketFromFile(self,ports,path):
        returnValue = dict()
        foundFirstLine = False
        with open(self.constants.instancesFile, 'r') as f:
            lines = f.read().splitlines()
            for first_line in lines:
                if (foundFirstLine):
                    break
                for port in ports:
                    if(port not in first_line):
                        continue
                    else:
                        foundFirstLine = True
                        curlResponse = self.sendCurlRequest(first_line, path, True)
                        returnValue['responseCode'] = self.processedCurlResponseCode(curlResponse)
                        if ( returnValue['responseCode'] == 'OK'):
                            if 'html' in str(curlResponse.headers.get('content-type')):
                                selection = self.parseHTMLForMethods(curlResponse.text)
                                if(selection is not None):
                                    returnValue['url'] = selection.replace('shouldInvokeMethod', 'invokeMethod')
                                else:
                                    returnValue['responseCode'] = 'ERROR'
                                    returnValue['error'] = 'Wrong Input'
        return returnValue



    def curlOnAllSocketsFromFile(self, path):
        with open(self.constants.instancesFile,'r') as fileName:
            lines = fileName.read().splitlines()
            for line in lines:
                curlResponse = self.sendCurlRequest(line, path, False)
                print(line  + ":" + self.processedCurlResponseCode(curlResponse) )

    def processedCurlResponseCode(self, curlResponse):
        try:
            status_code = curlResponse.status_code
            if(str(status_code) in self.httpConstants.responseCodeDictionary.keys()):
                return self.httpConstants.responseCodeDictionary.get(str(status_code))
            else:
                return 'UNKNOWN'
        except AttributeError:
            print("ERROR::Curl Response doesn't have attributes")
            return 'UNKNOWN'


    def sendCurlRequest(self,socket,component_path, basePath):
        dyn_admin_url = 'http://' + socket
        if(basePath):
            dyn_admin_url += self.constants.basePath

        dyn_admin_url += component_path
        try:
            curlResponse = requests.get(dyn_admin_url, auth=HTTPBasicAuth(self.constants.userName, self.constants.password ), timeout=5)
            if( self.processedCurlResponseCode(curlResponse) == 'OK'):
             #Good to parse the payload
                return curlResponse
            else:
                return None
        except (requests.exceptions.ConnectionError):
            print("ERROR:: Connection issues on " + socket)
            return None


    def parseHTMLForMethods(self, payload):
        soup = BeautifulSoup(payload, 'html.parser')
        # Look for methods and property names
        methodDict = dict()
        propertyDict = dict()

        for table in soup.find_all('table'):
            rows = table.find_all('tr')
            for row in rows:
                anchors = row.find_all('a')
                for anchor in anchors:
                    if ('?propertyName' in anchor['href']):
                        propertyName = re.compile(".*propertyName=(.*)$").match(anchor['href']).group(1)
                        if(len(propertyName) > 0):
                            propertyDict[propertyName] = anchor['href']
                    elif ('?shouldInvokeMethod' in anchor['href']):
                        methodName = re.compile(".*shouldInvokeMethod=(.*)$").match(anchor['href']).group(1)
                        if(len(methodName) > 0):
                            methodDict[methodName] = anchor ['href']
        return self.menuOutandSelect(methodDict)

    def menuOutandSelect(self, dynAdminDict):
        print("Choose from the following:")
        counter = 1
        inputStr = ''
        choiceDict = dict()
        for func in dynAdminDict:
            inputStr += ("\n " + str(counter) + ". " + func)
            choiceDict[counter] = func
            counter += 1
        response = input (inputStr)


        retryLimit=3
        while (retryLimit > 0):
            retryLimit -= 1
            if(response not in choiceDict.keys()):
                print ("ERROR:: Wrong Choice !! Pls choose again")
                response = input (inputStr)
                if(retryLimit == 0):
                    return None
                else:
                    continue
            else:
                break

        return(dynAdminDict.get(choiceDict.get(int(response))))

    def invokeMethod(self, path):
        response = input ("Pick up the instances you want to run \n\t 1.cap \n\t 2.commerce")
        ports = self.constants.instanceDictionary.get(self.constants.responseDictionary.get(response, '6'), 'None')
        # First curl on first socket to get all the methods
        response  = self.curlOnFirstSocketFromFile(ports, path)
        if(response.get('responseCode') == 'OK' and response.get('url') and not str(response.get('url')).isspace()):
            self.curlOnAllSocketsFromFile(response.get('url'))
        else:
            print(response.get('responseCode') + "::" + " Exiting..")


def main():

    calleeObj = CurlCallee()
    calleeObj.copyInstancesFileToLocal()
    #calleeObj.invokeMethod(calleeObj.constants.browsePageServiceFlushPath)
