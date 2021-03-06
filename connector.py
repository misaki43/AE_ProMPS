# -*- coding: utf-8 -*-

import pdb
import yarp
import numpy as np

#### pour tester : 
#connex = Connector()
#yarp.Time.delay(0.5)
#floatMessage = [0.0,1.0,2.0,3.0,1.,2.,3.]
#for i in range (10):
    #connex.addFloat(floatMessage)
    #yarp.Time.delay(0.5)
#myData = connex.readFloat()
#msg = "je m'appelle oriane"
#connex.addMessage(msg)
#connex.closeConnector()

class Connector():
    """Classe s'occupant des connexions yarp (read, write) avec Matlab avec :
    - port de lecture pr connecté à /Matlab:o
    - port d'écriture pw connecté à /Matlab:i"""

    def __init__(self, namePortToRead='/matlab/write',  namePortToWrite='/matlab/HP'):
        """"Connexion entre :
        - /VTSFE/state:o et namePortToWrite 
        - namePortToRead et /VTSFE/latentSpace:i"""

        yarp.Network.init()
        self.pw = yarp.BufferedPortBottle()
        self.pw.open('/ae/state:o')
        self.portMatlabOutput = namePortToRead
        self.portMatlabInput = namePortToWrite
        self.pr = yarp.BufferedPortBottle()
        self.pr.open('/ae/latentSpace:i')
        
        yarp.Network.connect(self.portMatlabOutput, self.pr.getName())
        yarp.Network.connect(self.pw.getName(),self.portMatlabInput)

    def closeConnector(self):
        yarp.Time.delay(0.5)    
        self.pr.close()
        self.pw.close()
        yarp.Network.fini()

    def addMessage(self, dataString):
        """Envoi un message"""
        self.message = self.pw.prepare()
        self.message.clear()
        self.message.addString(dataString)
        self.pw.write()

    def addFloat(self, dataFloat):
        """Envoi un ensemble de flottant contenu dans un tableau ou une liste"""
        self.message = self.pw.prepare()
        self.message.clear()
        for i in range(len(dataFloat)):
            self.message.addDouble(dataFloat[i])
        self.pw.write()

    def readFloat(self, nbData = [70,2], flag_debug =False):
        """Lis un ensemble de flottant et les renvoit dans une liste"""
        data = np.zeros(nbData)
        if(len(data[0]) ==1):
            b_in = self.pr.read()
            data = b_in.toString().split(' ')
            for i in range(len(data)):
                data[i]  = float(data[i])
        else:
            for i in range(nbData[0]):
                print(i)
                b_in = self.pr.read()
                data[i,:] = b_in.toString().split(' ')
        print('End traj')
        return data
