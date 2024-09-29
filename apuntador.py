import graphviz as graph
import os
class nodo:  # El nodito
    def __init__(self, dato, siguiente=None, anterior=None):
        self.dato = dato  # Datos
        self.siguiente = siguiente  # apuntadores
        self.anterior = anterior

#Es basicamente el mismo código de mi proyecto anterior pero con doblemente anidado
#Ya lo había hecho así que lo uso xd

class listita:  # La listita para las filas
    def __init__(self, inicio=None, fin=None, tamaño=0):  # El constructor de la lista
        self.inicio = inicio
        self.fin = fin
        self.tamaño = tamaño

    def agregar(self, dato):  # Función para agregar un nodo a la lista
        nuevo = nodo(dato)  # Creo el nodo con la información y el estado
        if self.tamaño == 0:  # si no hay nada, el inicio es igual al nuevo nodo
            self.inicio = nuevo
            self.fin = nuevo  # Igual que el final porque solo hay uno
            self.tamaño += 1  # Y el tamaño de la lista sería 1
        else:
            aux = self.inicio
            while (
                aux.siguiente != None
            ):  # Si el siguiente no está vacío, osea que no es el último
                aux = aux.siguiente  # Avanzo al siguiente
            nuevo.anterior = aux  # Coloco el apuntador al anterior
            aux.siguiente = nuevo  # Ya en el lugar, lo coloco en su posición de nuevo
            self.fin = nuevo
            self.tamaño += 1  # aumento el tamaño

    def mostrar(self):  # La verdad no sirve para nada pero me gusta verlo :)
        aux = self.inicio
        while aux != None:
            print(aux.dato)
            aux = aux.siguiente

    def retornar(self):
        aux = self.inicio
        while aux is not None:
            yield aux.dato  # Retorna el dato del nodo actual
            aux = aux.siguiente

    def modificar(self, pos, dato):  # Para modificar un dato en una posición indicada
        aux = self.inicio
        cont = 0
        while cont < pos:  # Llegando a la posición indicada
            aux = aux.siguiente
            cont += 1
        aux.dato = dato

    def encontrar(self, pos):  # Función para encontrar un dato en una posición indicada
        aux = self.inicio
        cont = 0
        while cont < pos:  # Solo me regresa el nodo a partir de la posición indicada
            aux = aux.siguiente  # Aquí llego a la posición
            cont += 1
        return aux.dato  # Retorno el nodo que deseo
    
    def concatenarF(self): #Función para que la fila sea una sola línea
        aux = self.inicio
        cadena = ""
        while aux != None:
            cadena += str(aux.dato) #proceso de concatenación por cada elemento de la fila
            aux = aux.siguiente
        return cadena

    def vaciar(self):
        self.inicio = None
        self.fin = None
        self.tamaño = 0
    
    def eliminar(self, pos):
        if pos >= self.tamaño or pos < 0:  # Verifico si la posición es válida
            return
        aux = self.inicio
        cont = 0
        while cont < pos:
            aux = aux.siguiente
            cont += 1
        if aux == self.inicio:
            self.inicio = aux.siguiente
            if self.inicio:
                self.inicio.anterior = None
        elif aux == self.fin:
            self.fin = aux.anterior
            if self.fin:
                self.fin.siguiente = None
        else:
            aux.anterior.siguiente = aux.siguiente
            aux.siguiente.anterior = aux.anterior
        self.tamaño -= 1


class maquina:
    def __init__(self,nombre,lineas,listadoProductos,tiempo,cantidadC):
        self.nombre=nombre
        self.lineas=int(lineas)
        self.listadoProductos=listadoProductos
        self.tiempo=int(tiempo)
        self.cantidadC=int(cantidadC)


class brazo:
    def __init__(self,nombre):
        self.nombre=nombre
        self.posicionActual=0
        self.estado=False
        self.bloqueo=False
        self.mensaje="No hacer nada"


class producto:
    def __init__(self,nombre,elaboracion):
        self.nombre=nombre
        self.elaboracion=elaboracion


class simulacion:
    def __init__(self, maquina, producto):  # Constructor de la simulación para UN PRODUCTO
        self.maquina = maquina
        self.producto = producto
        self.tiempo = 0
        self.elaborar = self.crearLista()
        self.posicionesBrazos = self.crearLineas()
        self.listaElab=self.crearLista2()
        self.coldDown = 0
        self.reporte=None
        self.matriz=None
        self.tiempoOptimo=0
        self.elaboOptima=False

    # Función para crear la lista de elaboración
    def crearLista(self):
        listaElaborar = listita()
        instrucciones = self.producto.elaboracion.split()
        for i in instrucciones:
            tupla = listita()  # Creo una lista para guardar la instrucción

            #Divido las intrucciones en L y C
            divi=i.split("C")

            l =int(divi[0][1:]) # Línea
            tupla.agregar(l)
            c = int(divi[1])  # Componente
            tupla.agregar(c)
            listaElaborar.agregar(tupla) # Agrego la instrucción a la lista
        return listaElaborar
    
    #Crea una copia de la lista pero sin la tupla (no es tupla de verdad aclaro xd)
    def crearLista2(self):
        listaelab=listita()
        instrucciones = self.producto.elaboracion.split()
        for i in instrucciones:
            listaelab.agregar(i)
        return listaelab

    # Función para crear la lista de brazos en las líneas
    def crearLineas(self):
        listaBrazos = listita()
        for i in range(self.maquina.lineas):
            brazo_linea = brazo(i + 1)  # Creamos un brazo para cada línea
            listaBrazos.agregar(brazo_linea)
        return listaBrazos

    # Función principal que simula el proceso
    def simular(self):
        cuenta = 0  # Contador de tiempo
        self.elaboOptima=True
        # Mientras haya elementos en la lista de elaboración
        ensamble = False
        nombreBloqueado = ""
        eliminar=False
        banderlistaelab=False

        
        Tiempos=listita() #Creo una Lista para guardar los datos de las listas
        while self.elaborar.tamaño > 0 or self.coldDown >= 0: # Mientras haya elementos en la lista de elaboración
            cuenta += 1 # Aumentamos el tiempo

            print(self.coldDown)

            print(f"Tiempo: {cuenta}")  # Imprimir el tiempo
            tiempo=listita() #Creo una lista para guardar los datos de las líneas
            tiempo.agregar(cuenta) #Agrego el tiempo a la lista

            #ciclo para desocupar los brazos y limpiar los mensajes
            for i in range(self.posicionesBrazos.tamaño): # Recorremos la lista de brazos
                brazo=self.posicionesBrazos.encontrar(i) # Ubico el brazo

                if brazo.nombre != nombreBloqueado: # Si el brazo bloqueado es el que se está buscando
                    brazo.estado=False # Lo desocupo
                    brazo.mensaje="No hacer nada"
                else:
                    brazo.estado=False # Lo ocupo

            #Comprobando que se halla pasado ya la posición necesaria para eliminar el procedimiento
            if banderlistaelab:
                self.listaElab.eliminar(0)
                banderlistaelab=False    

            # Recorremos la lista de elaboración
            for i in range(self.elaborar.tamaño):
                instruccion = self.elaborar.encontrar(i)  # Ubico la tupla
                linea = instruccion.encontrar(0)  # Línea
                componente = instruccion.encontrar(1)  # Componente
                print(f"Línea: {linea} Componente: {componente}")

                # Recorremos la lista de brazos
                for j in range(self.posicionesBrazos.tamaño):
                    brazo = self.posicionesBrazos.encontrar(j)  # Ubico el brazo

                    if brazo.nombre == linea:
                        print(f"Brazo: {brazo.nombre} en la línea {brazo.posicionActual}")
                        if not brazo.estado and ( not brazo.bloqueo):  # Si el brazo está desocupado
                            brazo.estado = True  # Lo ocupo
                            
                            if brazo.posicionActual < componente:  # Si la posición actual es menor al componente
                                
                                if not brazo.bloqueo:  # Si no está bloqueado
                                    brazo.posicionActual += 1  # Avanzo el brazo
                                    brazo.mensaje= f"Mover brazo - componente {brazo.posicionActual}" #Guardo el mensaje
                                    print(f"Brazo: {brazo.nombre} avanzando a la posición {brazo.posicionActual}")

                            elif brazo.posicionActual == componente:  # Si estamos en el componente
                                if not ensamble and (i==0):  # Si no se está ensamblando
                                    ensamble = True  # Se ensambla
                                    brazo.mensaje= f"Ensamblar componente {brazo.posicionActual}" #Guardo el mensaje
                                    print(brazo.mensaje)

                                    brazo.bloqueo = True  # El brazo se desocupa
                                    nombreBloqueado = brazo.nombre # Guardo el nombre del brazo bloqueado

                                    posParaEliminar = i # Guardo la posición para eliminar
                                    eliminar=True # Elimino la tarea

                                    #self.elaborar.eliminar(i)  # Eliminamos la tarea completada
                                    self.coldDown = self.maquina.tiempo-1  # Iniciamos el tiempo de espera
                                else:
                                    print("Ensamble en proceso o a la espera de ensamble")
                            else:  # Si la posición actual es mayor al componente
                                if not brazo.bloqueo: # Si no está bloqueado
                                    brazo.posicionActual -= 1  # Retrocedemos el brazo
                                    brazo.mensaje= f"Mover brazo - componente {brazo.posicionActual}" #Guardo el mensaje
                                    print(brazo.mensaje)



            if eliminar: # Si se debe eliminar la tarea
                self.elaborar.eliminar(posParaEliminar) # Eliminamos la tarea completada
                eliminar=False # Ya no se debe eliminar
                print("Tarea eliminada")

            # Control de tiempo de espera (coldown)
            if self.coldDown > 0:
                print(f"Enfriamiento: {self.coldDown}")
                self.coldDown -= 1
            else:
                self.coldDown = -1
                for j in range(self.posicionesBrazos.tamaño): # Recorremos la lista de brazos
                    brazo = self.posicionesBrazos.encontrar(j) # Ubico el brazo
                    if brazo.nombre == nombreBloqueado: # Si el brazo bloqueado es el que se está buscando
                        brazo.bloqueo = False # Se desbloquea
                        nombreBloqueado = "" 
                        banderlistaelab=True
                        print(f"Brazo {brazo.nombre} desbloqueado")
                        ensamble = False # Se desbloquea para que se pueda ensamblar

            #Ciclo para generar la lista de posiciones de los brazos
            for i in range(self.posicionesBrazos.tamaño): # Recorremos la lista de brazos
                brazo=self.posicionesBrazos.encontrar(i) # Ubico el brazo
                tiempo.agregar(brazo.mensaje) # Agrego el mensaje a la lista

            Tiempos.agregar(tiempo) # Agrego la lista de mensajes a la lista de tiempos

            print("------------------------------------------------------")
        self.matriz=Tiempos #Guardo la lista de tiempos en el reporte        
        

        #Probando que se guardó bien en la matriz :)
        for i in range(self.matriz.tamaño): # Recorremos la lista de tiempos
            for j in range(self.matriz.encontrar(i).tamaño):
                print(self.matriz.encontrar(i).encontrar(j), end=" | ") # Imprimimos el mensaje
            print() # Salto de línea
        #---------------------------------------------------------------------------------------
        self.tiempoOptimo=cuenta
        print(cuenta)

    def reportar(self): #Función para reportar el proceso
        self.reporte='<table style="width:100%; border: 1px solid black; border-collapse: collapse;"\n'
        self.reporte+='<tr>\n'
        self.reporte+='<th style="border: 1px solid black; text-align: center; padding: 8px;">Tiempo</th>\n'
        for i in range(self.maquina.lineas):
            self.reporte+='<th style="border: 1px solid black; text-align: center; padding: 8px;">Linea '+str(i+1)+'</th>\n'

        for i in range(self.matriz.tamaño): # Recorremos filas
            self.reporte+='<tr>\n'
            for j in range(self.matriz.encontrar(i).tamaño): # Recorremos las columnas de cada fila
                self.reporte+='<td style="border: 1px solid black; text-align: center; padding: 8px;">'+str(self.matriz.encontrar(i).encontrar(j))+'</td>\n'
            self.reporte+='</tr>\n'
        self.reporte+='<tr>\n'
        if self.elaboOptima:
            self.reporte+='<td style="border: 1px solid black; text-align: center; padding: 8px;" colspan="'+str(j+1)+'">El producto '+self.producto.nombre+' se puede elaborar óptimamente en '+str(i+1)+' segundos</td>\n'
        self.reporte+='</table>\n'
        print(self.reporte)

    def simularPorSegundos(self,segundos): #Función para simular el proceso por segundos
        cuenta = 0  # Contador de tiempo

        # Mientras haya elementos en la lista de elaboración
        ensamble = False
        nombreBloqueado = ""
        eliminar=False
        banderlistaelab=False
        
        Tiempos=listita() #Creo una Lista para guardar los datos de las listas
        while segundos>0: # Mientras el tiempo en el que quieren que se simule sea mayor a 0
            cuenta += 1 # Aumentamos el tiempo
            segundos-=1
            print(self.coldDown)

            print(f"Tiempo: {cuenta}")  # Imprimir el tiempo
            tiempo=listita() #Creo una lista para guardar los datos de las líneas
            tiempo.agregar(cuenta) #Agrego el tiempo a la lista

            #ciclo para desocupar los brazos y limpiar los mensajes
            for i in range(self.posicionesBrazos.tamaño): # Recorremos la lista de brazos
                brazo=self.posicionesBrazos.encontrar(i) # Ubico el brazo

                if brazo.nombre != nombreBloqueado: # Si el brazo bloqueado es el que se está buscando
                    brazo.estado=False # Lo desocupo
                    brazo.mensaje="No hacer nada"
                else:
                    brazo.estado=False # Lo ocupo
            
            #Comprobando que se halla pasado ya la posición necesaria para eliminar el procedimiento
            if banderlistaelab:
                self.listaElab.eliminar(0)
                banderlistaelab=False

            # Recorremos la lista de elaboración
            for i in range(self.elaborar.tamaño):
                instruccion = self.elaborar.encontrar(i)  # Ubico la tupla
                linea = instruccion.encontrar(0)  # Línea
                componente = instruccion.encontrar(1)  # Componente
                print(f"Línea: {linea} Componente: {componente}")

                # Recorremos la lista de brazos
                for j in range(self.posicionesBrazos.tamaño):
                    brazo = self.posicionesBrazos.encontrar(j)  # Ubico el brazo

                    if brazo.nombre == linea:
                        print(f"Brazo: {brazo.nombre} en la línea {brazo.posicionActual}")
                        if not brazo.estado and ( not brazo.bloqueo):  # Si el brazo está desocupado
                            brazo.estado = True  # Lo ocupo
                            
                            if brazo.posicionActual < componente:  # Si la posición actual es menor al componente
                                
                                if not brazo.bloqueo:  # Si no está bloqueado
                                    brazo.posicionActual += 1  # Avanzo el brazo
                                    brazo.mensaje= f"Mover brazo - componente {brazo.posicionActual}" #Guardo el mensaje
                                    print(f"Brazo: {brazo.nombre} avanzando a la posición {brazo.posicionActual}")

                            elif brazo.posicionActual == componente:  # Si estamos en el componente
                                if not ensamble and (i==0):  # Si no se está ensamblando
                                    ensamble = True  # Se ensambla
                                    brazo.mensaje= f"Ensamblar componente {brazo.posicionActual}" #Guardo el mensaje
                                    print(brazo.mensaje)

                                    brazo.bloqueo = True  # El brazo se desocupa
                                    nombreBloqueado = brazo.nombre # Guardo el nombre del brazo bloqueado

                                    posParaEliminar = i # Guardo la posición para eliminar
                                    eliminar=True # Elimino la tarea

                                    #self.elaborar.eliminar(i)  # Eliminamos la tarea completada
                                    self.coldDown = self.maquina.tiempo-1  # Iniciamos el tiempo de espera
                                else:
                                    print("Ensamble en proceso o a la espera de ensamble")
                            else:  # Si la posición actual es mayor al componente
                                if not brazo.bloqueo: # Si no está bloqueado
                                    brazo.posicionActual -= 1  # Retrocedemos el brazo
                                    brazo.mensaje= f"Mover brazo - componente {brazo.posicionActual}" #Guardo el mensaje
                                    print(brazo.mensaje)
            


            if eliminar: # Si se debe eliminar la tarea
                self.elaborar.eliminar(posParaEliminar) # Eliminamos la tarea completada
                eliminar=False # Ya no se debe eliminar
                print("Tarea eliminada")

            # Control de tiempo de espera (coldown)
            if self.coldDown > 0:
                print(f"Enfriamiento: {self.coldDown}")
                self.coldDown -= 1
            else:
                self.coldDown = -1
                for j in range(self.posicionesBrazos.tamaño): # Recorremos la lista de brazos
                    brazo = self.posicionesBrazos.encontrar(j) # Ubico el brazo
                    if brazo.nombre == nombreBloqueado: # Si el brazo bloqueado es el que se está buscando
                        brazo.bloqueo = False # Se desbloquea
                        nombreBloqueado = "" 
                        banderlistaelab=True

                        print(f"Brazo {brazo.nombre} desbloqueado")
                        ensamble = False # Se desbloquea para que se pueda ensamblar

            #Ciclo para generar la lista de posiciones de los brazos
            for i in range(self.posicionesBrazos.tamaño): # Recorremos la lista de brazos
                brazo=self.posicionesBrazos.encontrar(i) # Ubico el brazo
                tiempo.agregar(brazo.mensaje) # Agrego el mensaje a la lista

            Tiempos.agregar(tiempo) # Agrego la lista de mensajes a la lista de tiempos

            print("------------------------------------------------------")
        self.matriz=Tiempos #Guardo la lista de tiempos en el reporte        
        

        #Probando que se guardó bien en la matriz :)
        for i in range(self.matriz.tamaño): # Recorremos la lista de tiempos
            for j in range(self.matriz.encontrar(i).tamaño):
                print(self.matriz.encontrar(i).encontrar(j), end=" | ") # Imprimimos el mensaje
            print() # Salto de línea
        #---------------------------------------------------------------------------------------
        self.tiempoOptimo=cuenta
        #print(self.elaborar.encontrar(0).encontrar(0),self.elaborar.encontrar(0).encontrar(1))
        #self.listaElab.mostrar()

    def graficar(self): #Función para graficar el proceso
        grafo=graph.Digraph(format='png',name='Proceso de Sumulación')
        grafo.attr('node',shape='rectangle') #Atributo para que los nodos sean rectangulares
        grafo.attr(rankdir='LR') #Atributo para que los nodos se acomoden de izquierda a derecha
        paula=None
        for i in range(self.listaElab.tamaño): # Recorremos la lista de tiempos
            grafo.node(str(i),self.listaElab.encontrar(i)) # genero el nodo
            if paula!=None: # Si no es el primer nodo
                grafo.edge(str(paula),str(i)) # Creo la arista
            paula=i # Guardo el nombre del nodo anterior
        ruta=os.path.join('static','simulacion')
        grafo.render(ruta) #Genero el archivo pdf



    

    



