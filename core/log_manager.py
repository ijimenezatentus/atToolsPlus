import logging
import logging.handlers


class LogManager(object):

    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)
        if self._log.handlers == []:
            handler = logging.handlers.SysLogHandler(address = '/dev/log')
            self._log.addHandler(handler)

        

    def logInfo(self, informationMessage, transmitter):
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
        self._log.info("[{}] {}".format(transmitter, informationMessage))

    def logError(self, errorMessage, transmitter):
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.ERROR)
        self._log.error("[{}] {}".format(transmitter, errorMessage))

    def logDebug(self, debugMessage, transmitter):
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
        self._log.debug("[{}] {}".format(transmitter,  debugMessage))

    def logWarning(self, warningMessage, transmitter):
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.WARNING)
        self._log.warning("[{}] {}".format(transmitter, warningMessage))

    def logCritical(self, criticalMessage, transmitter):
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.CRITICAL)
        self._log.critical("[{}] {}".format(transmitter, criticalMessage))

