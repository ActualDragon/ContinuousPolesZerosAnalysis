'''Módulo desarrollado por Mauricio de Garay Hernández y Daniela Gómez Peniche
Fecha de entrega: 13/05/2020
En este módulo sirve como el controlador principal del programa en tiempo continuo
'''

import tkinter as tk
from FrameCoordenadas import FramePrincipal
from FuncionesVista import Funciones_V as Funciones
principal=tk.Tk()
principal.geometry=("800x800+100+0")
principal.resizable(False, False)
app = FramePrincipal(principal) #Crear la interfaz con el usuario en principal
principal.bind("<Return>", Funciones.MostrarResultados) #Mostrar los resultados cuando el usuario da enter
principal.mainloop()
