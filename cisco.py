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
#This method allows you to see the whole output and disabled paging in the terminal
def disable_Paging(remoteConnect):
    remoteConnect.send("terminal length 0\n")

#This method displays the disabled and unconnected ports of the interface in question. 
def sho_IP_Brief(remoteConnect):
        remoteConnect.send("sho int status | i notconnect | disabled\n")
        time.sleep(5)
        output = remoteConnect.recv(5000)
        return output.decode()



#For Debugging Purposes: Display all output without the algorithim bias - This one will be what works
def getInterfaceNames(remoteConnect):
    output = sho_IP_Brief(remoteConnect)
    linesOfOutput = output.split('\n')
    interfaces = []
    i = 0
    while i <= len(linesOfOutput)-1:
        interFaceID = linesOfOutput[i].split(' ')
        if "/" in interFaceID[0]:
            interfaces.append(interFaceID[0])
        i += 1
    return interfaces

# This will apply the change based on the interfaces in the output field. 
def convertInterfaceToVlan(listOfInterfaces, remoteConnect):
    remoteConnect.send('\n')
    for i in range(len(listOfInterfaces)):
        remoteConnect.send('config t\n')
        print("Sending ",listOfInterfaces[i], ' to vlan 666')
        remoteConnect.send('interface ' + listOfInterfaces[i] + '\n')
        remoteConnect.send('switchport access vlan 666\n')
        remoteConnect.send('do wr\n')
        remoteConnect.send('end\n')
        remoteConnect.send('exit\n')

# This is the main method, everything that needs to run, should go here
def mainMethod(host):
    isConnectionEstablished = False
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

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

#Script Executes Here
'''
We need to look into implementing a massive loop to parse through all of the nodes on the network and implement them into the mainMethod(IP).
'''

host = ['10.31.252.11', '10.31.252.11', '10.31.252.11']
if __name__=='__main__':
    for i in range(len(host)):
        mainMethod(host[i])
