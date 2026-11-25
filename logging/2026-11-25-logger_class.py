# Logger simple con niveles y formato configurable
import datetime

class Logger:
    LEVELS = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3}

    def __init__(self, name: str, level: str = 'INFO', log_file: str = None):
        self.name = name
        self.min_level = self.LEVELS[level]
        self.log_file = log_file

    def _log(self, level: str, msg: str):
        if self.LEVELS[level] < self.min_level: return
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f'[{ts}] [{level}] [{self.name}] {msg}'
        print(line)
        if self.log_file:
            with open(self.log_file, 'a') as f: f.write(line + '\n')

    def debug(self, msg):   self._log('DEBUG', msg)
    def info(self, msg):    self._log('INFO', msg)
    def warning(self, msg): self._log('WARNING', msg)
    def error(self, msg):   self._log('ERROR', msg)

log = Logger('App', level='DEBUG')
log.info("Servidor iniciado en puerto 3000")
log.warning("Alta latencia detectada")
log.error("Conexion a base de datos fallida")
