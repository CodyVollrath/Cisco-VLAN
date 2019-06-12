'''Program: CISCO IOS SCRIPT
Function: Automate VLAN port 666 to unconnected or disabled ports
Date: 06-06-2019
Corporation: Southwire Company
Author: Cody Vollrath
'''
import paramiko
import sys
import time
import os
from subprocess import call

def disable_Paging(remoteConnect):
    remoteConnect.send("terminal length 0\n")
    time.sleep(1)
def sho_IP_Brief(remoteConnect):
        remoteConnect.send('\n')
        remoteConnect.send("sho int status | i notconnect | disabled\n\n")
        time.sleep(5)
        output = remoteConnect.recv(5000)
        return output.decode()

#Gets the interface names from disabled ports
def getInterfaceNames(remoteConnect):
    output = sho_IP_Brief(remoteConnect)
    linesOfOutput = output.split('\n')
    interfaces = []
    i = 4

    while i <= len(linesOfOutput)-3:
        interFaceID = linesOfOutput[i].split(' ')
        interfaces.append(interFaceID[0])
        i += 1
    return interfaces

def convertInterfaceToVlan(listOfInterfaces, remoteConnect):
    remoteConnect.send('\n')
    for i in range(len(listOfInterfaces)):
        if listOfInterfaces[i] != 'Fa0':
            remoteConnect.send('config t\n')
            print("Sending ",listOfInterfaces[i], ' to vlan 666')
            remoteConnect.send('interface ' + listOfInterfaces[i] + '\n')
            remoteConnect.send('switchport access vlan 666\n')
            remoteConnect.send('do wr\n')
            remoteConnect.send('end\n')

    time.sleep(5)        
    remoteConnect.send('\n')
    remoteConnect.send("sho int status | i notconnect | disabled\n\n")
    time.sleep(5)
    output = remoteConnect.recv(5000)
    print(output.decode())
    

if __name__ =='__main__':

    isConnectionEstablished = False
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    '''
    After this test script, use the data from SQL to populate 
    an array of nodes and use a for loop to instantiate it.
    '''
    host = '10.31.252.11'

    try:
        ssh.connect(host, port=22, username='Vollrathco', password='Xxtriggered_911xX!')
        time.sleep(5)
        print("Connected")
        isConnectionEstablished = True

    except:
        print("No connection")

    if isConnectionEstablished:
        sshConnect = ssh.invoke_shell()
        disable_Paging(sshConnect)
        intfaces = getInterfaceNames(sshConnect)
        print(intfaces)
        convertInterfaceToVlan(intfaces, sshConnect)
