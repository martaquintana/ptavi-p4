#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import json
import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    SIP Register server class
    """
    dic_clients = {}
    expires = ''
    def register2json(self):
        """
        JSON file dictionary
        """
        json.dump(self.dic_clients, open('registered.json','w'))
    
    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"Hemos recibido tu peticion ")
        for line in self.rfile:
            linea_decod = line.decode('utf-8').split(" ")
            
            if linea_decod[0] == 'REGISTER':
                
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                client_sip = linea_decod[1].split(":")
                sip_address = client_sip[1]
                self.dic_clients[sip_address] = [self.client_address[0]]
            if linea_decod[0] == 'Expires:':
                self.expires = linea_decod[1][:-2]
                self.dic_clients[sip_address] += [self.expires]
                if self.expires == '0':
                    del self.dic_clients[sip_address] 
                
                
                
           
            print(self.dic_clients)      
        print(self.client_address[0])
        print((self.client_address[1]))
        
if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the SIPRegisterHandler class to manage the request
    try:
        port = int(sys.argv[1])
        serv = socketserver.UDPServer(('', port), SIPRegisterHandler) 
    
        print("Lanzando servidor UDP de eco...")
        try:
            serv.serve_forever()
        except KeyboardInterrupt:
            print("Finalizado servidor")
    except:
        print("Usage: phython3 server.py puerto")
