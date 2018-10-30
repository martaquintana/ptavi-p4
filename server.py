#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import json
import socketserver
import sys
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    SIP Register server class
    """
    dic_clients = {}

    def register2json(self):
        """
        JSON file
        """
        json.dump(self.dic_clients, open('registered.json', 'w'))

    def json2register(self):
        """
        Open JSON file and gets the dictionary
        """
        try:
            with open('registered.json', 'r') as fich:
                self.dic_clients = json.load(fich)
        except (FileNotFoundError, ValueError, json.decoder.JSONDecodeError):
            pass

    def whohasexpired(self):
        """
        Search and delete the clients expired
        """
        del_list = []
        now = time.strftime(
                            '%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        for clients in self.dic_clients:
            if self.dic_clients[clients]["expires"] <= now:
                del_list.append(clients)
        for clients in del_list:
            del self.dic_clients[clients]

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        if self.dic_clients == {}:
            self.json2register()
        self.wfile.write(b"Hemos recibido tu peticion ")
        for line in self.rfile:
            linea_decod = line.decode('utf-8').split(" ")

            if linea_decod[0] == 'REGISTER':
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                client_sip = linea_decod[1].split(":")
                sip_address = client_sip[1]
                self.dic_clients[sip_address] = {
                                     "address": self.client_address[0]
                                     }
            if linea_decod[0] == 'Expires:':
                expires = linea_decod[1][:-2]
                then = time.strftime(
                        '%Y-%m-%d %H:%M:%S', time.gmtime(
                                time.time() + float((expires))))
                self.dic_clients[sip_address]["expires"] = then
                if expires == '0':
                    del self.dic_clients[sip_address]
                else:
                    self.whohasexpired()
        print("Nuevo usuario registrado")
        self.register2json()


if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the SIPRegisterHandler class to manage the request
    try:
        port = int(sys.argv[1])
        serv = socketserver.UDPServer(('', port), SIPRegisterHandler)
        print("Lanzando servidor UDP...")
        try:
            serv.serve_forever()
        except KeyboardInterrupt:
            print("Finalizado servidor")
    except (IndexError, ValueError, PermissionError):
        print("Usage: phython3 server.py puerto")
