from excecoes.window_closed import WindowClosed
from controladores.controlador_central import ControladorCentral

try:
    ControladorCentral().inicia()
except WindowClosed:
    quit()