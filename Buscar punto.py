#Percerptron(Más o menos)
import turtle as t
import random as r
import math

#Funciones 

#Para ver si se acerca o se aleja
def HaPasadoCerca(PuntosCercanos, lista):
    for row in lista:
        if row[0] >= PuntosCercanos[1][0] and row[0] <= PuntosCercanos[0][0] and row[1] <= PuntosCercanos[1][1] and row[0] >= PuntosCercanos[2][1]:
            return True
    return False

def HaPasadoLejos(PuntosLejanos, lista):
    for row in lista:
        if row[0] <= PuntosLejanos[1][0] or row[0] >= PuntosLejanos[0][0] or row[1] >= PuntosLejanos[1][1] or row[0] <= PuntosLejanos[2][1]:
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

#Inteno fallido
def DistribuirProb(probAr, probAb, probD, probI, arriba, abajo, derecha, izquierda):
    res = r.randint(1, 10)
    
    if abajo > arriba:
        probAr = probAr * res
        probAb = probAb / res
    else:
        probAr = probAr / res
        probAb = probAb * res
        
    if derecha > izquierda:
        probI = probI * res
        probD = probD / res
    else:
        probI = probI / res
        probD = probD * res

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

conseguido = False

#Registros
probAr = 0.5
probAb = 0.5
probD = 0.5
probI = 0.5

RegPuntos = []
PuntosCercanos = []
RegProb = []


arriba = 0
abajo = 0
derecha = 0
izquierda = 0


#Preparativos para la búsqueda
while not conseguido:
    
    #Dibuja
    t.clear()
    Centrar()
    
    limites(x)
    DibujarPunto(punto)
    PuntosCercanos = CuadradoCercano(punto)
    PuntosLejanos = CuadradoLejano(punto, x)

    #Distribuye probavilidades según si ha pasado cerca o no
    if HaPasadoCerca(PuntosCercanos, RegPuntos):
        res = r.randint(0, 10)/40
        
        if abajo > arriba and probAb + res <= 1:
            probAr = probAr - res
            probAb = probAb + res
        else:
            probAr = probAr + res
            probAb = probAb - res

        res = r.randint(0, 10)/40
        
        if derecha > izquierda and probD + res <= 1:
            probI = probI - res
            probD = probD + res
        else:
            probI = probI + res
            probD = probD - res

        
        
    elif HaPasadoLejos(PuntosLejanos, RegPuntos):

        #Si te has hacercado recientemente, repites su probavilidad
        if not(RegProb == []):
            probAr = RegProb[0]
            probAb = RegProb[1]
            probI = RegProb[2]
            probD = RegProb[3]
        
        else:
            res = r.randint(0, 10)/20
            
            if abajo > arriba and probAr + res <= 1:
                probAr = probAr + res
                probAb = probAb - res
            else:
                probAr = probAr - res
                probAb = probAb + res

            res = r.randint(0, 10)/40
            
            if derecha > izquierda and probI + res <= 1:
                probI = probI + res
                probD = probD - res
            else:
                probI = probI - res
                probD = probD + res

    else:
        res = r.randint(0, 10)/20
        
        if abajo > arriba and probAr + res <= 1:
            probAr = probAr + res
            probAb = probAb - res
        else:
            probAr = probAr - res
            probAb = probAb + res

        res = r.randint(0, 10)/40
        
        if derecha > izquierda and probI + res <= 1:
            probI = probI + res
            probD = probD - res
        else:
            probI = probI - res
            probD = probD + res

    #Inicializa registros de los pasos que ha dado
    arriba = 0
    abajo = 0
    derecha = 0
    izquierda = 0
    contador = 0

    #Entra en el bucle en el que busca
    continuar = True
    while continuar:
        
        #Inicializa tiempo de búsqueda y puntos por los que ha pasado
        contador += 1
        RegPuntos = []

        #Da pasos según la probavilidad y guarda el punto al que llega en RegPuntos
        i = r.randint(0, 100)
        if i <= 100 * probD:  
            Derecha()
            derecha += 1
        else:    
            Izquierda()
            izquierda += 1

        puntoP = [round(t.xcor()), round(t.ycor())]
        if not EstaEnLista(RegPuntos, puntoP):
            RegPuntos.append(puntoP)
        
        if i <= 100 * probAr:    
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
        if round(t.xcor()) == punto[0] and round(t.ycor()) == punto[1]:
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
    print("\nProb de ir a:\n  Abajo: " + str(probAb) + "\n  Arriba: " + str(probAr) + "\n  Izquierda: " + str(probI) + "\n  Derecha: " + str(probD))
    if HaPasadoCerca(PuntosCercanos, RegPuntos) and HaPasadoLejos(PuntosLejanos, RegPuntos):
        print("\nMucha vuelta")
    elif HaPasadoLejos(PuntosLejanos, RegPuntos):
        print("\nNi te has acercado")
    elif HaPasadoCerca(PuntosCercanos, RegPuntos):
        RegProb = [probAr, probAb, probI, probD]
        print("\nHas estado cerca")
    else:
        print("\nSin mas")

    


if conseguido:
    print("\n\nYa lo has encontrado bro")

    
#Voy a editar un poco esto a ver que lo que
