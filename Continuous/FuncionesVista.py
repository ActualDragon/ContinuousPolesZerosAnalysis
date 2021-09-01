'''Módulo desarrollado por Mauricio de Garay Hernández y Daniela Gómez Peniche
Fecha de entrega: 13/05/2020
En este módulo se obtiene la información de la vista principal, se calculan, se grafican y se despliegan las respuestas del programa en tiempo continuo
'''

import tkinter as tk
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageTk
from scipy import signal
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.widgets import Slider

#Modelo
class Funciones_V:
    x=0 
    y=0
    Opcion="Tache" #El default de selección es un polo
    VentanaActual="Coordenadas"
    ArregloPolos=[0,0,0,0,0]
    ArregloCeros=[0,0,0,0,0]
    ContadorPolos=0
    ContadorCeros=0
    numerador1=[]
    denominador1=[]
    Hz=""
    StringEc=""
    @staticmethod #Hacer método estático
    def MostrarResultados(OrigenEvento):
        if Funciones_V.VentanaActual=="Coordenadas":
            if Funciones_V.ContadorCeros>Funciones_V.ContadorPolos:
                messagebox.showerror("Sistema sin sentido físico.", "ERROR: Los ceros seran más que los polos. No tiene sentido físico.")
                return
            numerador=[]
            # tenemos H(s)=((s-C0)+....(s-Cn))/((s-P0)+....(s-Pn))
            #desarrolar numerador
            b=0 #Bandera del numerador
            if Funciones_V.ContadorCeros==0:
                numerador.append(1) #Si no hay ceros el numerador es 1
                b=1
            if Funciones_V.ContadorCeros==1: #Si hay un cero
                numerador=[1,-1*Funciones_V.ArregloCeros[0]]
                b=2
            if Funciones_V.ContadorCeros==2: #Si hay dos ceros
                N0=np.convolve([1, -1*Funciones_V.ArregloCeros[0]], [1, -1*Funciones_V.ArregloCeros[1]])
                numerador=N0
                b=3
            if Funciones_V.ContadorCeros==3: #Si hay tres ceros
                N0=np.convolve([1, -1*Funciones_V.ArregloCeros[0]], [1, -1*Funciones_V.ArregloCeros[1]])
                N1=np.convolve(N0, [1, -1*Funciones_V.ArregloCeros[2]])
                numerador=N1
                b=4
            if Funciones_V.ContadorCeros==4: #Si hay cuatro ceros
                N0=np.convolve([1, -1*Funciones_V.ArregloCeros[0]], [1, -1*Funciones_V.ArregloCeros[1]])
                N1=np.convolve(N0, [1, -1*Funciones_V.ArregloCeros[2]])
                N2=np.convolve(N1, [1, -1*Funciones_V.ArregloCeros[3]])
                numerador=N2
                b=5
            if Funciones_V.ContadorCeros==5: #Si hay cinco ceros
                N0=np.convolve([1, -1*Funciones_V.ArregloCeros[0]], [1, -1*Funciones_V.ArregloCeros[1]])
                N1=np.convolve(N0, [1, -1*Funciones_V.ArregloCeros[2]])
                N2=np.convolve(N1, [1, -1*Funciones_V.ArregloCeros[3]])
                N3=np.convolve(N2, [1, -1*Funciones_V.ArregloCeros[4]])
                numerador=N3
                b=6
            numerador=np.around(numerador,4) #Redondear para que se vea bonito
            #Lo mismo pero con denominador
            denominador=[]
            b1=0 #Bandera del denominador
            if Funciones_V.ContadorPolos==0: #Si no hay polos
                denominador.append(1)
                b1=1
            if Funciones_V.ContadorPolos==1: #Si hay un polo
                denominador=[1,-1*Funciones_V.ArregloPolos[0]]
                b1=2
            if Funciones_V.ContadorPolos==2: #Si hay dos polos
                N0=np.convolve([1, -1*Funciones_V.ArregloPolos[0]], [1, -1*Funciones_V.ArregloPolos[1]])
                denominador=N0
                b1=3
            if Funciones_V.ContadorPolos==3: #Si hay tres polos
                N0=np.convolve([1, -1*Funciones_V.ArregloPolos[0]], [1, -1*Funciones_V.ArregloPolos[1]])
                N1=np.convolve(N0, [1, -1*Funciones_V.ArregloPolos[2]])
                denominador=N1
                b1=4
            if Funciones_V.ContadorPolos==4: #Si hay cuatro polos
                N0=np.convolve([1, -1*Funciones_V.ArregloPolos[0]], [1, -1*Funciones_V.ArregloPolos[1]])
                N1=np.convolve(N0, [1, -1*Funciones_V.ArregloPolos[2]])
                N2=np.convolve(N1, [1, -1*Funciones_V.ArregloPolos[3]])
                denominador=N2
                b1=5
            if Funciones_V.ContadorPolos==5: #Si hay cinco polos
                N0=np.convolve([1, -1*Funciones_V.ArregloPolos[0]], [1, -1*Funciones_V.ArregloPolos[1]])
                N1=np.convolve(N0, [1, -1*Funciones_V.ArregloPolos[2]])
                N2=np.convolve(N1, [1, -1*Funciones_V.ArregloPolos[3]])
                N3=np.convolve(N2, [1, -1*Funciones_V.ArregloPolos[4]])
                denominador=N3
                b1=6
            denominador=np.around(denominador,4) #Redondear el denominador
            print(denominador)
            ventana2=tk.Tk()
            #ya tenemos la funcion de transferencia
            stringHz="H(s)=\\frac{"
            i=0
            #Hacer el string de la función de transferencia
            if b==1:
                stringNum="1}{"   
                stringHz=stringHz+stringNum
            if b>1:
                exponente=numerador.size-1
                stringNum=""
                while i<numerador.size:
                    if i==numerador.size-1: #Si es mi último valor del numerador lo agrego al final
                        aux="{}s^{}".format(np.real(numerador[i]),exponente)
                        aux=aux+"}{"
                        stringNum=stringNum+aux
                        exponente=exponente-1
                    else: #Si no es mi último valor del numerador agrego el valor y después un +
                        aux="{}s^{} +".format(np.real(numerador[i]),exponente)
                        exponente=exponente-1
                        stringNum=stringNum+aux
                    i=i+1
                stringHz=stringHz+stringNum
            i=0
            if b1==1:
                stringDenom="1}" #Si el valor es 1
                stringHz=stringHz+stringDenom
            if b1>1:
                exponente=denominador.size-1
                stringDenom=""
                while i<denominador.size:
                    if i==denominador.size-1:
                        aux="{}s^{}".format(np.real(denominador[i]),exponente)
                        aux=aux+"}"
                        exponente=exponente-1
                        stringDenom=stringDenom+aux
                    else:
                        aux="{}s^{} +".format(np.real(denominador[i]),exponente)
                        exponente=exponente-1
                        stringDenom=stringDenom+aux
                    i=i+1
                stringHz=stringHz+stringDenom

            #Ya sabemos la ecuacion de diferencias.
            Funciones_V.Hz=stringHz
            BotonHz=tk.Button(ventana2, text="Ver H(s)", command=Funciones_V.VerHz)
            BotonHz.pack()
            stringEc="" #String que guarda la ecuación de diferencias
            i=0
            #Armar ecuación de diferencias
            if b1==1:
                stringY="y(t)=" #Si el denominador es uno
                stringEc=stringEc+stringY
            if b1>1:
                stringY=""
                while i<denominador.size:
                    derivada=""
                    j=denominador.size-1
                    while j>i:
                        derivada=derivada+"'"
                        j=j-1
                    if i==denominador.size-1:
                        igual="(t)="
                        aux="{}y".format(np.real(denominador[i]))+derivada+igual
                        stringY=stringY+aux
                    else:
                        mas="(t)+"
                        aux="{}y".format(np.real(denominador[i]))+derivada+mas
                        stringY=stringY+aux
                    i=i+1
                stringEc=stringEc+stringY
            i=0
            if b==1:
                stringX="x(t)"   
                stringEc=stringEc+stringX
            if b>1:
                stringX=""
                while i<numerador.size:
                    derivada=""
                    j=numerador.size-1
                    while j>i:
                        derivada=derivada+"'"
                        j=j-1
                    if i==numerador.size-1:
                        punto="(t)."
                        aux="{}x".format(np.real(numerador[i]))+derivada+punto
                        stringX=stringX+aux
                    else:
                        mas="(t)+"
                        aux="{}x".format(np.real(numerador[i]))+derivada+mas
                        stringX=stringX+aux
                    i=i+1
                stringEc=stringEc+stringX
            
            Funciones_V.stringEc=stringEc
            BotonEc=tk.Button(ventana2, text="Ver ecuación diferencial.", command=Funciones_V.VerEcuacion)
            BotonEc.pack()
            #Ahora hay que obtener los coeficientes por fraccion parcial
            
            CajaR=tk.Frame(master=ventana2)
            CajaR.pack()
            r,p,k=signal.residue(numerador, denominador)
            print("Coeficientes:", r)
            print("Polos: ", p)
            print("Constante: ", k)
            #Obtener tiempo para graficar la respuesta
            lim=1000000
            for pp in p:
                if pp < lim:
                    lim = np.real(pp)
                    lim = np.absolute(lim)
                    if lim!=0:
                        lim = 5/lim
            if lim == 0:
                lim=20
            #Encontrar valor hasta el que irá el slider, si la duración es muy chica, no habrá slider
            bandera=0
            lim=lim*3
            if lim<1:
                bandera=1
            max=4*lim
            t=np.linspace(0, max, 1000)
            h=np.zeros(t.size)
            np.meshgrid(t,h)
            for rr,pp in zip(r,p):
                h=h+rr*np.exp(pp*t) #Armar ecuación
            hayk=0
            for kk in k:
                    hayk=1
            if hayk==1:
                messagebox.showinfo("No es fracción parcial", ("Hay una {}d(t) en el instante t=0 que no será graficada.").format(k[0]))
            
            f = plt.Figure()
            eje=f.add_subplot(111,title="h(t) (y) vs t (x)")
            eje.plot(t,h)
            #Que la vista default llegue hasta la duración de la respuesta al impulso calculada
            eje.set_xlim(0,lim)
            eje.axhline()
            eje.grid()
            caja1=tk.Frame(master=CajaR)
            labelt=tk.Label(caja1, text="Respuesta al impulso: ")
            labelt.pack()
            caja1.pack(side=tk.LEFT)
            canvas = FigureCanvasTkAgg(f, master=caja1)  # A tk.DrawingArea.
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            #Slider tiempo
            if bandera==0:
                eje_hor=f.add_axes([0.12,0.1,0.78,0.03]) #Delimitar el eje del slider
                #El slider estará centrado con t máximo=duración de respuesta al impulso calculada, avanzará
                #esa duración/10 y llega hasta t máximo=duración*4s
                s_hor=Slider(eje_hor,'Max t',0, max,valinit=lim, valstep=lim/10) #Crear el slider
                def update(val): #Función que actualiza el valor del slider
                    pos=int(s_hor.val)
                    if pos>0:
                        eje.set_xlim(0,pos)
                    f.canvas.draw_idle()
                s_hor.on_changed(update)
            
            
            toolbar = NavigationToolbar2Tk(canvas, caja1)
            toolbar.update()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)


            

            
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
           #respuesta al escalón
           
            #esto es  u(s)= 1/s, tienes que convolve denom/num con esto, hacer signal.residue de eso, y luego sumar los coeficientes*e^polotiempo. 
            #Similar a lo que se hace arriba con h(t)
            escalonLaplace=[1,0]
            sn=np.zeros(t.size)
            np.meshgrid(t,sn)
            denominadorLaplace=np.convolve(denominador, escalonLaplace)
            r1,p1,k1=signal.residue(numerador, denominadorLaplace)
            hayk=0
            for rr,pp in zip(r1,p1):
                sn=sn+rr*np.exp(pp*t) #Armar la respuesta al escalón

            #INICIO GRÁFICAS RESPUESA AL ESCALÓN
            f1 = plt.Figure()
            eje1=f1.add_subplot(111, title="S(t) (y) vs t (x)")
            eje1.plot(t,sn)
            eje1.set_xlim(0,lim)
            eje1.axhline()
            eje1.grid()
            caja=tk.Frame(master=CajaR)
            labelsn=tk.Label(caja, text="Respuesta al escalón")
            labelsn.pack()
            caja.pack(side=tk.RIGHT)
            canvas2 = FigureCanvasTkAgg(f1, master=caja)  # A tk.DrawingArea.
            canvas2.draw()
            canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            if bandera==0: #Hacer slider si no es muy corta la respuesta
                eje_hor1=f1.add_axes([0.12,0.1,0.78,0.03]) #Delimitar el eje del slider
                #El slider estará centrado con t máximo=duración de respuesta al impulso calculada, avanzará
                #esa duración/10 y llega hasta t máximo=duración*2
                s_hor1=Slider(eje_hor1,'Max t',0, max,valinit=lim, valstep=lim/10) #Crear el slider
                #Función cuando el slider es utilizado
                def update1(val): #Actualizar el valor del slider conforme se mueve
                    pos=int(s_hor1.val)
                    if pos>0:
                        eje1.set_xlim(0,pos)
                    f1.canvas.draw_idle()
                s_hor1.on_changed(update1)
            toolbar2 = NavigationToolbar2Tk(canvas2, caja)
            toolbar2.update()
            canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
            Funciones_V.numerador1=numerador
            Funciones_V.denominador1=denominador
            botonF=tk.Button(master=ventana2, text="Respuesta en Frecuencia", command= Funciones_V.VerRespuestaF)
            botonF.pack()
            
            ventana2.mainloop()
            Funciones_V.VentanaActual="Resultados"
        else:
            exit()
    @staticmethod
    def VerHz():
        #Ajustar tamaño de letra de la función de transferencias dependiendo tamaño de numerador/denominador y coeficientes
        font=25
        inicioX=0.2
        if Funciones_V.numerador1.size>3:
            font=18
            inicioX=0
        for rr in Funciones_V.numerador1:
            if np.abs(rr)>1000:
                font=18
                inicioX=0
            if np.abs(rr)>10000:
                font=15
                inicioX=0
            if np.abs(rr)>100000:
                font=10
                inicioX=0
        if Funciones_V.denominador1.size>3:
            font=18
            inicioX=0
        for rr in Funciones_V.denominador1:
            if np.abs(rr)>1000:
                font=18
                inicioX=0
            if np.abs(rr)>10000:
                font=15
                inicioX=0
            if np.abs(rr)>100000:
                font=10
                inicioX=0
        ventana=tk.Tk()
        label = tk.Label(ventana)
        label.pack()
        ventana.geometry("1200x800")
        fig = Figure(figsize=(20, 20), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=label)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        texto="$"+Funciones_V.Hz+"$"
        ax.clear()
        ax.text(inicioX, 0.6, texto, fontsize = font)  
        canvas.draw()
    @staticmethod
    def VerEcuacion():
        #Ajustar tamaño de letra de la ecuación diferencial dependiendo tamaño de coeficientes
        font=20
        inicioX=0.2
        if Funciones_V.numerador1.size>3:
            font=10
            inicioX=0
        for rr in Funciones_V.numerador1:
            if np.abs(rr)>1000:
                font=15
                inicioX=0
            if np.abs(rr)>10000:
                font=10
                inicioX=0
            if np.abs(rr)>100000:
                font=8.35
                inicioX=0
        if Funciones_V.denominador1.size>3:
            font=10
            inicioX=0
        for rr in Funciones_V.denominador1:
            if np.abs(rr)>1000:
                font=15
                inicioX=0
            if np.abs(rr)>10000:
                font=10
                inicioX=0
            if np.abs(rr)>100000:
                font=8.35
                inicioX=0
        ventana=tk.Tk()
        label = tk.Label(ventana)
        label.pack()
        ventana.geometry("1200x800")
        fig = Figure(figsize=(20, 20), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=label)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        #Separar lado x de lado y para que uno este por encima del otro y tener mejor formato
        t1=Funciones_V.stringEc.split("=")
        texto="$"+t1[0]+"="+"$\n"+"$"+t1[1]+"$"
        ax.clear()
        ax.text(inicioX, 0.6, texto, fontsize = font)  
        canvas.draw()
    @staticmethod
    def VerRespuestaF():
        #Ver escala Respuesta en F.
        #Recorreremos TODOS los polos y ceros, veremos cuál tiene la parte imaginaria más grande y w irá hasta 2x eso.
        ListaPolosYCeros=[]
        for C in Funciones_V.ArregloCeros:
            ListaPolosYCeros.append(C)
        for P in Funciones_V.ArregloPolos:
            ListaPolosYCeros.append(P)
        #Ya se tiene una lista con todos los polos y ceros, ahora veremos cuál es el valor imaginario mayor
        Mayor=0
        for pp in ListaPolosYCeros:
            if np.abs(np.imag(pp))>Mayor:
                Mayor=np.abs(np.imag(pp))
        MaximoW=0
        if Mayor<1:
            MaximoW=30
        else:
            MaximoW=Mayor*15
        numerador=Funciones_V.numerador1
        denominador=Funciones_V.denominador1
        #Ahora hay que obtener la respuesta en frecuencia
        ventana3=tk.Tk()
        CajaF=tk.Frame(master=ventana3)
        CajaF.pack()
        bandera=0
        if(MaximoW<400):
            w=np.linspace(0,400,1200)
            bandera=0
        else:
            w=np.linspace(0,MaximoW*1.5,1200)
            bandera=1

        Caja1=tk.Frame(master=CajaF)
        Caja1.pack(side=tk.LEFT)
        
        H=np.polyval(numerador, 1j*w)/np.polyval(denominador, 1j*w)
        #Graficas respuesta en frecuencia y slider para ajustar frecuencia
        f2 = plt.Figure()
        eje=f2.add_subplot(111, xlabel="Frecuencia", ylabel="Amplitud", title="Frecuencia (x) vs Amplitud (y)")
        eje.plot(w, np.abs(H))
        eje.set_xlim(0.1,MaximoW)
        eje.grid()
        eje.set_xscale("log")
        labelF=tk.Label(Caja1, text="Respuesta en Frecuencia Amplitud(usa slider para ajustar hasta dónde va w):")
        labelF.pack()
        canvas3 = FigureCanvasTkAgg(f2, master=Caja1)  # A tk.DrawingArea.
        canvas3.draw()
        canvas3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        #Slider
        eje_hor=f2.add_axes([0.12,0.1,0.78,0.03]) #Delimitar el eje del slider
        if bandera==0:
            s_hor=Slider(eje_hor,'Max W',0, 400,valinit=MaximoW, valstep=1) #Crear el slider
        else:
            s_hor=Slider(eje_hor,'Max W',0, MaximoW*1.5,valinit=MaximoW, valstep=1) #Crear el slider

        def update(val): #Actualizar la gráfica conforme se mueve el slider
            pos=int(s_hor.val)
            if pos>0:
                eje.set_xlim(0.1,pos)
            f2.canvas.draw_idle()
        s_hor.on_changed(update)
        toolbar3 = NavigationToolbar2Tk(canvas3, Caja1)
        toolbar3.update()
        canvas3.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        #Graficar respuesta en frecuencia
        Caja2=tk.Frame(master=CajaF)
        Caja2.pack(side=tk.RIGHT)
        labelF=tk.Label(Caja2, text="Respuesta en Frecuencia Fase(usa slider para ajustar hasta dónde va w):")
        labelF.pack()
        f3 = plt.figure()
        eje2=f3.add_subplot(111, xlabel="Frecuencia", ylabel="Fase", title="Frecuencia (x) vs Fase(y)")
        eje2.plot(w, np.angle(H)/np.pi)
        eje2.set_xscale("log")
        eje2.set_xlim(0.1,MaximoW)
        eje2.grid()
        canvas4 = FigureCanvasTkAgg(f3, master=Caja2)  # A tk.DrawingArea.
        canvas4.draw()
        canvas4.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        toolbar4 = NavigationToolbar2Tk(canvas4, Caja2)
        toolbar4.update()
        canvas4.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        #Slider
        eje_hor2=f3.add_axes([0.12,0.1,0.78,0.03]) #Delimitar el eje del slider
        if bandera==0:
            s_hor2=Slider(eje_hor2,'Max W',0, 400,valinit=MaximoW, valstep=1) #Crear el slider
        else:
            s_hor2=Slider(eje_hor2,'Max W',0, MaximoW*1.5,valinit=MaximoW, valstep=1) #Crear el slider

        def update2(val): #Actualizar la gráfica cuando se mueve el slider
            pos=int(s_hor2.val)
            if pos>0:
                eje2.set_xlim(0.1,pos)
            f3.canvas.draw_idle()
        s_hor2.on_changed(update2)
        ventana3.title("Respuesta en Frecuencia")
        ventana3.mainloop()
    @staticmethod
    def BotonCeroClick():
         Funciones_V.Opcion="Corazon" #Cambiar a selección de ceros si se da click en el corazón
         print("Cora")
    @staticmethod
    def BotonPoloClick():
         Funciones_V.Opcion="Tache" #Regresar a polos si se da click en el tache
         print("Tache")





