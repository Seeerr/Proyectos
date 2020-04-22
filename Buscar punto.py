#Percerptron(Más o menos)
import turtle as t
import random as r
import math

#Funciones 

#Para ver si se acerca o se aleja(Esto es lo que tiene pinta de estar mal)
def HaPasadoCerca(PuntosCercanos, lista):
    for row in lista:
        if row[0] >= PuntosCercanos[1][0] and row[0] <= PuntosCercanos[0][0] and row[1] <= PuntosCercanos[1][1] and row[1] >= PuntosCercanos[2][1]:
            return True
    return False

def HaPasadoLejos(PuntosLejanos, lista):
    for row in lista:
        if row[0] <= PuntosLejanos[1][0] or row[0] >= PuntosLejanos[0][0] or row[1] >= PuntosLejanos[1][1] or row[1] <= PuntosLejanos[2][1]:
            return True
    return False

#Mira si un punto ya esta en una lista de puntos
def EstaEnLista(lista, punto):
    for row in lista:
        if row[0] == punto[0] and row[1] == punto[1]:
            return True

#Centra al bicho
def Centrar():
    t.up()
    t.setx(0)
    t.sety(0)
    t.down()
    
#Crea límites de búsqueda
def limites(x):
    esquinas = []
    t.seth(0)
    t.up()
    t.fd(x/2)
    t.lt(90)
    t.fd(x/2)
    t.lt(90)
    t.down()
    for i in range(0, 4):
        esquinas.append([round(t.xcor()), round(t.ycor())])
        t.fd(x)
        t.lt(90)
    Centrar()
    return esquinas

#Pasos que puede dar el bicho
def Izquierda():
    t.seth(180)
    t.fd(10)

def Arriba():
    t.seth(90)
    t.fd(10)
    
def Abajo():
    t.seth(270)
    t.fd(10)
    
def Derecha():
    t.seth(0)
    t.fd(10)

#Crea un punto
def Punto():
    print("Introduce las coordenadas del punto(Múltiplos de 10)")
    cordx = int(input("Coordenada x: "))
    cordy = int(input("Coordenada y: "))
    punto = [cordx, cordy]
    return punto

#Dibuja un punto
def DibujarPunto(punto):
    t.up()
    t.setx(punto[0])
    t.sety(punto[1])
    t.down()
    limites(5)

#Inteno fallido(RegProb = [probAr, probAb, probI, probD])
def DistribuirProbAFabor(RegProb, arriba, abajo, derecha, izquierda, cantidad):
    res = 10
    if RegProb[0] + res > 1:
        res = r.randint(0, 10)/cantidad
        
    if abajo > arriba:
        RegProb[0] = RegProb[0] - res
        RegProb[1] = RegProb[1] + res
    else:
        RegProb[0] = RegProb[0] + res
        RegProb[1] = RegProb[1] - res

    res = 10
    if RegProb[3] + res > 1:
        res = r.randint(0, 10)/cantidad
        
    if derecha > izquierda:
        RegProb[2] = RegProb[2] - res
        RegProb[3] = RegProb[3] + res
    else:
        RegProb[2] = RegProb[2] + res
        RegProb[3] = RegProb[3] - res

    return RegProb

def DistribuirProbEnContra(RegProb, arriba, abajo, derecha, izquierda, cantidad):
    res = 10
    if RegProb[0] + res > 1:
        res = r.randint(0, 10)/cantidad
        
    if abajo > arriba:
        RegProb[0] = RegProb[0] + res
        RegProb[1] = RegProb[1] - res
    else:
        RegProb[0] = RegProb[0] - res
        RegProb[1] = RegProb[1] + res

    res = 10
    if RegProb[2] + res > 1:
        res = r.randint(0, 10)/cantidad
        
    if derecha > izquierda:
        RegProb[2] = RegProb[2] + res
        RegProb[3] = RegProb[3] - res
    else:
        RegProb[2] = RegProb[2] - res
        RegProb[3] = RegProb[3] + res

    return RegProb

def CambiarProb(RegProb):
    aux = RegProb[0]
    RegProb[0] = RegProb[1]
    RegProb[1] = aux
    aux = RegProb[2]
    RegProb[2] = RegProb[3]
    RegProb[3] = aux

#Dibujar cuadrado cercano al punto y dar esquinas
def CuadradoCercano(punto):
    t.color("green")
    t.up()
    t.setx(punto[0])
    t.sety(punto[1])
    t.down()
    res = limites(100)
    t.color("black")
    return res

#Dibujar cuadrado lejano
def CuadradoLejano(punto, x):
    t.color("red")
    t.up()
    t.setx(punto[0])
    t.sety(punto[1])
    t.down()
    res = limites(x)
    t.color("black")
    return res




#MAIN
x = int(input("Introduce los limites de movimiento(Recomendado 700): "))
punto = Punto()
t.speed(0)

conseguido = False

#Registros
RegProb = [0.5, 0.5, 0.5, 0.5]   #(RegProb = [probAr, probAb, probI, probD])
RegPuntos = []
PuntosCercanos = []
ProbCercana = []   #Registro base de probavilidades con las que más se acerca


arriba = 0
abajo = 0
derecha = 0
izquierda = 0
intentos =0


#Preparativos para la búsqueda
while not conseguido:
    intentos += 1
    
    #Dibuja
    t.clear()
    Centrar()
    
    limites(x)
    DibujarPunto(punto)
    PuntosCercanos = CuadradoCercano(punto)
    PuntosLejanos = CuadradoLejano(punto, x)

    #MODIFICAR PROBAVILIDADES SEGÚN LO QUE HA PASADO
    
    #Se ha alejado
    if HaPasadoLejos(PuntosLejanos, RegPuntos):
        if ProbCercana == []:
            RegProb = DistribuirProbEnContra(RegProb, arriba, abajo, derecha, izquierda, 10)
        else:
            RegProb = ProbCercana
            ProbCercana = []
    #Ha pasado cerca
    elif HaPasadoCerca(PuntosCercanos, RegPuntos):
        i = r.randint(1, 10)
        if i % 2 == 0:
            RegProb = DistribuirProbAFabor(RegProb, arriba, abajo, derecha, izquierda, i * 10)
        else:
            RegProb = DistribuirProbEnContra(RegProb, arriba, abajo, derecha, izquierda, i * 10)
    #Si ha pasado o por las dos o por ninguna zona cítica
    else:
        RegProb = DistribuirProbEnContra(RegProb, arriba, abajo, derecha, izquierda, 40)

    #Inicializa registros de los pasos que ha dado
    arriba = 0
    abajo = 0
    derecha = 0
    izquierda = 0
    contador = 0
    RegPuntos = []

    #Entra en el bucle en el que busca
    continuar = True
    while continuar:
        
        #Inicializa tiempo de búsqueda y puntos por los que ha pasado
        contador += 1

        #Da pasos según la probavilidad y guarda el punto al que llega en RegPuntos
        i = r.randint(0, 100)
        if i <= 100 * RegProb[3]:  
            Derecha()
            derecha += 1
        else:    
            Izquierda()
            izquierda += 1

        puntoP = [round(t.xcor()), round(t.ycor())]
        if not EstaEnLista(RegPuntos, puntoP):
            RegPuntos.append(puntoP)

        #Encontrar
        encontrado1 = round(t.xcor()) == punto[0] and round(t.ycor()) == punto[1]
        
        if i <= 100 * RegProb[0]:    
            Arriba()
            arriba += 1
        else:    
            Abajo()
            abajo += 1

        puntoP = [round(t.xcor()), round(t.ycor())]
        if not EstaEnLista(RegPuntos, puntoP):
            RegPuntos.append(puntoP)

        #COSAS QUE LO SACAN DEL BUCLE DE BÚSQUEDA
        #Encontrar
        encontrado2 = round(t.xcor()) == punto[0] and round(t.ycor()) == punto[1]
        
        if encontrado1 or encontrado2:
            print("Lo has encontrado")
            continuar = False
            conseguido = True

        #controlar que no se salga
        if t.xcor() < -x/2 or t.xcor() > x/2 or t.ycor() < -x/2 or t.ycor() > x/2:
            print("Te has salido")
            continuar = False

        #Controlar tiempo
        if contador == 500:
            print("Esta dando vueltas")
            continuar = False

    #Un poco de información para el que lo ejecuta
    print("\nRegistro de movimientos:\n  Abajo: " + str(abajo) + "\n  Arriba: " + str(arriba) + "\n  Izquierda: " + str(izquierda) + "\n  Derecha: " + str(derecha))
    print("\nProb de ir a:\n  Abajo: " + str(RegProb[1]) + "\n  Arriba: " + str(RegProb[0]) + "\n  Izquierda: " + str(RegProb[2]) + "\n  Derecha: " + str(RegProb[3]))
    if HaPasadoCerca(PuntosCercanos, RegPuntos) and HaPasadoLejos(PuntosLejanos, RegPuntos):
        print("\nMucha vuelta")
    elif HaPasadoLejos(PuntosLejanos, RegPuntos):
        print("\nNi te has acercado")
    elif HaPasadoCerca(PuntosCercanos, RegPuntos):
        ProbCercana = RegProb
        print("\nHas estado cerca")
    else:
        print("\nSin mas")

    


if conseguido:
    print("\n\nYa lo has encontrado bro\n Lo ha encontrado en " + str(intentos) "intentos")
