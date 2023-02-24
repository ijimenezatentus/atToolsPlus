
import json
import subprocess
from core.log_manager import LogManager

"""
    @package core
    ===============
    @file   at_tracert.py
    @author Ivan Jimenez A. <ijimenez@atentus.com>
            (c) Servicios de Monitoreo S.A. - Santiago, Chile
    @brief  Clase encargada de utilizar herramienta mtr (Tracert) 
    @date   Feb/2021
"""

class AtTracert():

    def tracert(self,host,ciclos,tiempofuera):
        
        self._log = LogManager()
        self._log.logInfo('Realizando Dig', self.__class__.__name__)
        print("Realizando Tracert")
        
        try:

            resultado = subprocess.check_output(["mtr", "-c " + ciclos,"-j", host],timeout = tiempofuera)

            #Si mtr no encuentra el host indica "mtr: Failed to resolve host: atrgfgfentus.com: Name or service not known"
            #pero la respuesta esta vacia
            if str(resultado) == "b''":
                
                self._log.logInfo("error:Host no encontrado", self.__class__.__name__)
                reply = '{"codigo_error":"1","error":"Host no encontrado"}'

            else:

                resultado = resultado.decode('utf8').replace("'", '"')
                data = json.loads(resultado)
                reply = json.dumps(data, sort_keys=True)
                          
            
                       
        except subprocess.TimeoutExpired as e:
            print("error timeout")
            self._log.logInfo("error timeout", self.__class__.__name__)
            reply ='{"error":"Timeout excedido"}'

        self._log.logInfo("Tracert terminado", self.__class__.__name__)
        print("Tracert terminado\n")
        
        
        return reply
