#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os

entrada = sys.argv

class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        #self.wfile.write("Hemos recibido tu peticion")
        lista = ['INVITE', 'ACK', 'BYE']
        while 1:
            line = self.rfile.read()
            recibido = line.split(' ')
            print recibido[0]
            if not line:
                break
            if entrada[0] == 'INVITE':
                sentencia = 'SIP/2.0 100 Trying\r\n\r\n'
                sentencia += 'SIP/2.0 180 Ring\r\n\r\n'
                sentencia += 'SIP/2.0 200 OK\r\n\r\n'
                print sentencia
                self.wfile.write(sentencia)
            elif recibido[0] == 'ACK':
                aEjecutar = 'mp32rtp -i ' + entrada[1] + ' -p ' + entrada[2] + ' < ' + entrada[3]
                os.system(aEjecutar)
            elif recibido[0] not in lista:
                print 'SIP/2.0 405 Method Not Allowed\r\n\r\n'
                self.wfile.write('SIP/2.0 405 Method Not Allowed\r\n\r\n')
            else:
                print 'SIP/2.0 400 Badrequest\r\n\r\n'
                self.wfile.write("SIP/2.0 400 bad request\r\n\r\n")

if __name__ == "__main__":
    
    if len(entrada) != 4:
        sys.exit('Usage: python server.py IP port audio_file')

    serv = SocketServer.UDPServer(("", int(entrada[2])), EchoHandler)
    print "Listening..."
    serv.serve_forever()
