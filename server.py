#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de SIP
"""

import SocketServer
import sys
import os

entrada = sys.argv


class SIPHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server class
    """

    def handle(self):
        lista = ['INVITE', 'ACK', 'BYE']
        IP_CLIENT = str(self.client_address[0])
        while 1:
            line = self.rfile.read()
            recibido = line.split(' ')
            print recibido[0]
            if not line:
                break
            if recibido[0] == 'INVITE':
                sentencia = 'SIP/2.0 100 Trying\r\n\r\n'
                sentencia += 'SIP/2.0 180 Ringing\r\n\r\n'
                sentencia += 'SIP/2.0 200 OK\r\n\r\n'
                print sentencia
                self.wfile.write(sentencia)
            elif recibido[0] == 'ACK':
                aEjecutar = './mp32rtp -i ' + IP_CLIENT + ' -p 23032 < '
                aEjecutar += entrada[3]
                os.system('chmod 755 mp32rtp')
                os.system(aEjecutar)
                print "Finalizado envío"
            elif recibido[0] == 'BYE':
                sentencia = 'SIP/2.0 200 OK\r\n\r\n'
                print sentencia
                self.wfile.write(sentencia)
            elif recibido[0] not in lista:
                print 'SIP/2.0 405 Method Not Allowed\r\n\r\n'
                self.wfile.write('SIP/2.0 405 Method Not Allowed\r\n\r\n')
            else:
                print 'SIP/2.0 400 Bad Request\r\n\r\n'
                self.wfile.write("SIP/2.0 400 bad request\r\n\r\n")

if __name__ == "__main__":

    if len(entrada) != 4:
        sys.exit('Usage: python server.py IP port audio_file')

    serv = SocketServer.UDPServer((entrada[1], int(entrada[2])), SIPHandler)
    print "Listening..."
    serv.serve_forever()
