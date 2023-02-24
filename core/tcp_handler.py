import socketserver

"""
    @package core
    ===============
    @file   tcp_handler.py
    @author Ivan Jimenez A. <ijimenez@atentus.com>
            (c) Servicios de Monitoreo S.A. - Santiago, Chile
    @brief  Clase encargada de administrar los datos de entrada y salida desde diferentes conexiones
    @date   Feb/2021
"""

class TcpHandler(socketserver.BaseRequestHandler):
 
    def handle(self):
        #Recibe el dato de entrada
        data = self.request.recv(1024).decode().strip()
        msj = self.server.requestListener(self.client_address[0], data)
        #Envia respuesta del requerimiento
        
        self.request.send(msj.encode("utf-8"))
        #self.request.send(msj)
        print("Conexion Cerrada con Cliente {}".format(self.client_address[0]))

