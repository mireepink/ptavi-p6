#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion")
        while 1:
            line = self.rfile.read()
            entrada = line.split(' ')
            if entrada[0] == 'INVITE':
                sentencia = 'SIP/2.0 100 Trying\r\n\r\n'
                sentencia += 'SIP/2.0 180 Ring\r\n\r\n'
                sentencia += 'SIP/2.0 200 OK\r\n\r\n'
                print sentencia
                self.wfile.write(sentencia)
            elif entrada[0] != 'INVITE' or 'ACK' or 'BYE':
                print 'SIP/2.0 405 Method Not Allowed\r\n\r\n'
                self.wfile.write('SIP/2.0 405 Method Not Allowed\r\n\r\n')
            else:
                print 'SIP/2.0 400 Badrequest\r\n\r\n'
                self.wfile.write("SIP/2.0 400 bad request\r\n\r\n")
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    
    entrada = sys.argv
    
    if len(entrada) != 5:
        sys.exit('Usage: python server.py IP port audio_file')

    serv = SocketServer.UDPServer(("", int(entrada[4])), EchoHandler)
    print "Listening..."
    serv.serve_forever()
