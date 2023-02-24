

import socketserver
#import subprocess
import multiprocessing
import sys
import json
import configparser
import time
import datetime
import socket
from core.tcp_handler import TcpHandler
from core.at_ping import AtPing
from core.at_tracert import AtTracert
from core.at_dig import AtDig
from core.log_manager import LogManager


"""
    @package core
    ===============
    @file   attools.py
    @author Ivan Jimenez A. <ijimenez@atentus.com>
            (c) Servicios de Monitoreo S.A. - Santiago, Chile
    @brief  Clase principal y controladora del programa
    @date   Feb/2021
"""

# Solicitud de Ping
# ARQTTcpAtTools:1|@@| {"monitor": "192.168.2.2", "host": "atentus.com", "bytes":1, "key":"eef910ab4f71097ced27d1b9dbc94d4b", "ciclos":4, "timeout":20}


# Solicitud de Dig correcta
# ARQTTcpAtTools:2|@@| {"monitor": "192.168.2.2", "host": "atentus.com", "key":"eef910ab4f71097ced27d1b9dbc94d4b", "dns":"@8.8.8.8", "timeout":30}

# Solicitud de Tracert  (mtr)
# ARQTTcpAtTools:3|@@| {"monitor": "192.168.2.2", "host": "atentus.com", "key":"eef910ab4f71097ced27d1b9dbc94d4b", "ciclos":5, "timeout":20}


class ThreadServer (socketserver.ThreadingMixIn, socketserver.TCPServer):

    daemon_threads = True
    allow_reuse_address = True

    # Inicio de servicio
    def __init__(self, server_address, TcpHandler):
        self._log = LogManager()
        self._log.logInfo('Servidor TCP iniciado en: {}'.format(server_address), self.__class__.__name__)
        print('Servidor TCP iniciado en: {}'.format(server_address))
        socketserver.TCPServer.__init__(self, server_address, TcpHandler)

        print('Escuchando...')

    def requestListener(self, clientAddress, data):
        #print("Solicitud desde : " + clientAddress)
        self._log.logInfo(data, self.__class__.__name__)
        general = data.split("|@@|")
        error = "ARTTcpAtTools: 0|@@|" + \
                '{"codigo_error":"99", "error": "petición malformada"}\n'
        if len(general) > 1:

            cabecera = general[0].split(":")

            requerimiento = cabecera[0]

            tipo = cabecera[1]
            datos = json.loads(general[1])
            print(general[1])
            if requerimiento == "ARQTTcpAtTools":

                llaves = configparser.ConfigParser()

                llaves.read('/home/monitor/atToolsPlus/config/global.ini')

                llave_encontrada = False

                keys = json.loads(llaves.get("KEYS", "key"))
                for key in keys:
                    if key == datos["key"]:
                        llave_encontrada = True
                    break

                if llave_encontrada:
                    print("Llave encontrada")
                    mon = socket.gethostname()
                    
                    # 1 = Ping
                    if tipo == "1":
             
                        atping = AtPing()
                        tiempo_inicio = time.time()
                        
                        datos = atping.pings(datos["host"],str(datos["ciclos"]),str(datos["bytes"]),datos["timeout"])
                        tiempo_fin = time.time()
                        tiempo_respuesta = int(tiempo_fin - tiempo_inicio)

                    # 2 = Dig
                    if tipo == "2":
                        atdig = AtDig()
                        tiempo_inicio = time.time()
                        datos = atdig.dig(datos["host"], str(
                            datos["dns"]), datos["timeout"])

                        tiempo_fin = time.time()
                        tiempo_respuesta = int(tiempo_fin - tiempo_inicio)

                    # 3 = Tracert

                    if tipo == "3":
                        attracert = AtTracert()
                        tiempo_inicio = time.time()
                        datos = attracert.tracert(datos["host"], str(
                            datos["ciclos"]), datos["timeout"])

                        tiempo_fin = time.time()

                        tiempo_respuesta = int(tiempo_fin - tiempo_inicio)

                    reply = respuesta.responder(
                        self, tipo, datos, mon, tiempo_respuesta)
                else:
                    print("Error : Key Incorrecta")
                    error = "Error : Key Incorrecta \n"
                    reply = error
            else:
                self._log.logInfo(error, self.__class__.__name__)
                reply = error
        else:
            self._log.logInfo(error, self.__class__.__name__)
            reply = error
        return reply


class RunServer(multiprocessing.Process):

    def __init__(self):
        pass

    def run(self):

        try:

            self.tcpServer = ThreadServer(('0.0.0.0', 2000), TcpHandler)
            self.tcpServer.serve_forever()

            sys.stdout.flush()
        except Exception as e:
            print('Error: {}'.format(e))


class respuesta:
    def __init__(self):
        pass


    def responder(self,tipo, data, monitor, tiempo_resp):

        cabecera = 'ARTTcpAtTools: ' + tipo + ' |@@| '

        datos = {
            "data": json.loads(data),
            "monitor":  monitor,
            "fecha": str(datetime.datetime.now()),
            "tiempo_respuesta": tiempo_resp
        }

        datos = json.dumps(datos, sort_keys=True)
        reply = cabecera + datos + "\n"
        return reply
