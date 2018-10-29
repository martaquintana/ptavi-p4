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
    expires = ''
    now = ''
    list_sip_address=[]
    
    def register2json(self):
        """
        JSON file
        """
        json.dump(self.dic_clients, open('registered.json','w'))
        
    def whohasexpired(self):
		#Falta que borre del diccionario si ha expirado.
        print(self.now)
        for clients in self.list_sip_address:
            if str(self.dic_clients[clients]["expires"]) < str(self.now):
                 del self.dic_clients[clients]
                 print(self.list_sip_address.index(clients))
                 self.list_sip_address.remove(clients)
		
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
                self.list_sip_address.append(sip_address)
                self.dic_clients[sip_address] = {"address": self.client_address[0]}
            if linea_decod[0] == 'Expires:':
                self.expires = linea_decod[1][:-2]
                self.now = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(time.time()))
                then= time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(time.time() + float((self.expires))))
                print(self.now)
                print(then)
                self.dic_clients[sip_address]["expires"] = then
                if self.expires == '0':
                     del self.dic_clients[sip_address]
        self.whohasexpired()        
        print(self.dic_clients) 
        self.register2json()
        print(self.client_address[0])
        print((self.client_address[1]))
        self.whohasexpired()    

        
if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the SIPRegisterHandler class to manage the request
    try:
        port = int(sys.argv[1])
        serv = socketserver.UDPServer(('', port), SIPRegisterHandler) #'' escucha en todas las direcciones ip que tenga la maquina
    
        print("Lanzando servidor UDP de eco...")
        try:
            serv.serve_forever()
        except KeyboardInterrupt:
            print("Finalizado servidor")
    except:
        print("Usage: phython3 server.py puerto")

#ssh gamma07
#python3 servidor.py
#python client.py gamma07 6001
