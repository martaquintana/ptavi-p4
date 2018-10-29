#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

# Constantes y Variables.
# Dirección IP del servidor, puerto y contenido a enviar

SERVER = 'localhost'
try:
    ip = sys.argv[1]
    port = int(sys.argv[2])
    # line = ' '.join(sys.argv[3::])
    register = sys.argv[3]
    sip_address = sys.argv[4]
    expires = sys.argv[5]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.connect((SERVER, port))
        if register == 'register':
            line = (
                'REGISTER sip:' + sip_address
                + ' SIP/2.0\r\n' + 'Expires: ' + expires + '\r\n\r\n')
            print("Enviando:", line, end='')
            print(expires)
            my_socket.send(bytes(line, 'utf-8'))
            data = my_socket.recv(1024)
            print('Recibido -- ', data.decode('utf-8'), end='')
    print("Socket terminado.")

except (IndexError, ValueError):
    print("Usage:client ip puerto" + " register sip_address expires_value")

except ConnectionRefusedError:
    print("Servidor apagado")
