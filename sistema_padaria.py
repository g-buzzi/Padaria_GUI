from excecoes.WindowClosed import WindowClosed
from controladores.controlador_central import ControladorCentral

from controladores.controlador_ingredientes import ControladorIngredientes

try:
    ControladorCentral().inicia()
except WindowClosed:
    quit()


"""
ControladorCentral().inicia()
"""