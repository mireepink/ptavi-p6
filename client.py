#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

entrada = sys.argv

if len(entrada) != 4:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")
#Cuando no encuentra puerto Error: No server listening at 193.147.73.20 port 5555 ***Mirar excepcion

METODO = entrada[3]
direccion = entrada[4].split('@')
LOGIN_SERVER = direccion[0]
xxx = direccion[1].split(':')
IP_SERVER = xxx[0]
PUERTO_SERVER = xxx[1]

# Contenido que vamos a enviar
LINE = METODO + ' sip:' + LOGIN_SERVER + '@' + IP_SERVER + ' SIP/2.0' + '\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando: " + LINE
my_socket.send(LINE + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
