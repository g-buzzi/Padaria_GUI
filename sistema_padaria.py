from excecoes.WindowClosed import WindowClosed
from controladores.controlador_central import ControladorCentral

try:
    ControladorCentral().inicia()
except WindowClosed:
    quit()