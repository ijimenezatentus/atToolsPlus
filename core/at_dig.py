
import json
import subprocess
from core.log_manager import LogManager

"""
    @package core
    ===============
    @file   at_dig.py
    @author Ivan Jimenez A. <ijimenez@atentus.com>
            (c) Servicios de Monitoreo S.A. - Santiago, Chile
    @brief  Clase encargada de realizar dig a direccion indicada y devolver resultado
    @date   Feb/2021
"""

# Solicitud de Dig correcta
# ARQTTcpAtTools:2|@@| {"monitor": "192.168.2.2", "host": "microsoft.com", "key":"eef910ab4f71097ced27d1b9dbc94d4b", "dns":"@8.8.8.8", "timeout":30}


class AtDig():

    def dig(self, host, dns, tiempofuera):

        self._log = LogManager()
        self._log.logInfo('Realizando Dig', self.__class__.__name__)
       
        print("Realizando Dig")

        try:
          
            resultado = subprocess.check_output(
                ['dig' ,'+nocmd', '+nocomments', '+noquestion', '+noauthority', '+noadditional', host])
            prueba = resultado.splitlines()
            data =[]
            for x in prueba:
                if (x.decode('utf-8') != ''):
                    
                    if (x.decode('utf-8').find(";;")==-1):
                      
                        lineas = x.split(b'\t')
                        js =  {
                                "Name": lineas[0].decode('utf-8'),
                                "TTL": lineas[2].decode('utf-8'),
                                "Class": lineas[3].decode('utf-8'),
                                "Type": lineas[4].decode('utf-8'),
                                "IpAddress": lineas[5].decode('utf-8')
                            }
                        
                        data.append(js)
                    else:
                        dato = x.decode('utf-8').replace(";; ","")
                        dato = dato.split(":")
                        dato = {dato[0]:dato[1]}
                        data.append(dato)
            
            reply = (json.dumps(data))
        except subprocess.CalledProcessError as e:
            print("error codigo : " + str(e.returncode))
            self._log.logInfo('codigo_error":"1","error":"Host no encontrado', self.__class__.__name__)
            reply = '{"codigo_error":"1","error":"Host no encontrado"}'
        except subprocess.TimeoutExpired as e:
            print("error timeout")
            self._log.logInfo("error:Timeout excedido", self.__class__.__name__)
            reply = '{"codigo_error":"2","error":"Timeout excedido"}'

        self._log.logInfo('Dig terminado', self.__class__.__name__)
        print("Dig terminado\n")

        return reply
