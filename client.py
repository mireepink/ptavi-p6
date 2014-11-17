#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

entrada = sys.argv

if len(entrada) != 3:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")

METODO = entrada[1]
DIRECCION = entrada[2].split('@')
LOGIN_SERVER = DIRECCION[0]
IP_PUERTO = DIRECCION[1].split(':')
IP_SERVER = IP_PUERTO[0]
PUERTO_SERVER = int(IP_PUERTO[1])

LINE = METODO + ' sip:' + LOGIN_SERVER + '@' + IP_SERVER + ' SIP/2.0' + '\r\n'

try:

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP_SERVER, PUERTO_SERVER))

    print "Enviando: " + LINE
    my_socket.send(LINE + '\r\n')
    data = my_socket.recv(1024)

    print 'Recibido -- ', data
    sentencia = 'SIP/2.0 100 Trying\r\n\r\n'
    sentencia += 'SIP/2.0 180 Ring\r\n\r\n'
    sentencia += 'SIP/2.0 200 OK\r\n\r\n'

    if data == sentencia:
        LINE = 'ACK' + ' sip:' + LOGIN_SERVER + '@' + IP_SERVER + ' SIP/2.0' + '\r\n'
        print 'Enviando: ' + LINE
        my_socket.send(LINE + '\r\n')
        data = my_socket.recv(1024)
        print 'Recibido -- ', data

    print "Terminando socket..."

    my_socket.close()
    print "Fin."

except socket.error:

    print 'Error: No server listening at' + IP_SERVER + 'port' + PUERTO_SERVER
