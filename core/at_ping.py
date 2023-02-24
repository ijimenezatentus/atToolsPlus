import json
import subprocess
from core.log_manager import LogManager

"""
    @package core
    ===============
    @file   at_ping.py
    @author Ivan Jimenez A. <ijimenez@atentus.com>
            (c) Servicios de Monitoreo S.A. - Santiago, Chile
    @brief  Clase encargada de realizar ping y devolver resultado, necesita paquete pingparsing
    @date   Feb/2021
"""
# Solicitud de Ping
# ARQTTcpAtTools:1|@@| {"host": "www.google.com", "bytes":32, "key":"eef910ab4f71097ced27d1b9dbc94d4b", "ciclos":4, "timeout":20}

class AtPing():

    def pings(self,host,ciclos,bites,tiempofuera):
        self._log = LogManager()
        self._log.logInfo('Realizando Ping', self.__class__.__name__)


        if ciclos==0:
            ciclos=4
        if bites==0:
            bites=64

        try:

           # self._log.logInfo("ping -c " + str(ciclos) + " -s " +  str(bites) + " " + host, self.__class__.__name__)
            resultado = subprocess.check_output(["ping", "-c", str(ciclos),"-s", str(bites), host],timeout = tiempofuera)
            resultado = resultado.decode('utf8').replace("'", '"')
            s_res_a =resultado.split( "--- "+ host +" ping statistics ---")
            s_res_b = s_res_a[1].replace("\n","").split("rtt")
            s_res_c = s_res_b[0].split(", ")
            s_res_d = s_res_b[1].split(" = ")
            
            js =  {
                    "host" : host,
                    "packets transmitted" :  str(s_res_c[0].split(" ")[0] ),
                    "packets received" :  str(s_res_c[1].split(" ")[0] ),
                    "packets loss" : str(s_res_c[2].split(" ")[0] ),
                    "time " : str(s_res_c[3].split(" ")[1] ),
                    "rtt min" :  str(s_res_d[1].split("/")[0] ),
                    "rtt avg" : str(s_res_d[1].split("/")[1] ),
                    "rtt max" :  str(s_res_d[1].split("/")[2] ),
                    "rtt mdev" :  str(s_res_d[1].split("/")[3].replace(" ms","") )
                }
                            
           # print(json.dumps(js))
            reply = json.dumps(js, sort_keys=True)
           # print(reply)

        except subprocess.CalledProcessError as e:
            self._log.logInfo("error codigo : " + str(e.returncode), self.__class__.__name__)
            reply ='{"codigo_error":"1","error":"Host no encontrado"}'
        except subprocess.TimeoutExpired as e:
            self._log.logInfo("error timeout", self.__class__.__name__)
            reply = '{"codigo_error":"2","error":"Timeout excedido"}'

        self._log.logInfo('Ping terminado', self.__class__.__name__)
        print("Ping terminado\n")

        return reply
