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
        self.coldDown = 0

    # Función para crear la lista de elaboración
    def crearLista(self):
        listaElaborar = listita()
        instrucciones = self.producto.elaboracion.split()
        for i in instrucciones:
            tupla = listita()  # Creo una lista para guardar la instrucción
            l = int(i[1])  # Línea
            tupla.agregar(l)
            c = int(i[3])  # Componente
            tupla.agregar(c)
            listaElaborar.agregar(tupla)
        return listaElaborar

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

        # Mientras haya elementos en la lista de elaboración
        ensamble = False
        nombreBloqueado = ""
        eliminar=False
        while self.elaborar.tamaño > 0:
            cuenta += 1

            print(f"Tiempo: {cuenta}")  # Imprimir el tiempo

            #ciclo para desocupar los brazos
            for i in range(self.posicionesBrazos.tamaño):
                brazo=self.posicionesBrazos.encontrar(i)
                brazo.estado=False


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
                        if not brazo.estado:  # Si el brazo está desocupado
                            brazo.estado = True  # Lo ocupo
                            
                            if brazo.posicionActual < componente:  # Si la posición actual es menor al componente
                                
                                if not brazo.bloqueo:  # Si no está bloqueado
                                    brazo.posicionActual += 1  # Avanzo el brazo
                                    print(f"Brazo: {brazo.nombre} avanzando a la posición {brazo.posicionActual}")
                            elif brazo.posicionActual == componente:  # Si estamos en el componente
                                if not ensamble:  # Si no se está ensamblando
                                    ensamble = True  # Se ensambla
                                    print(f"Ensamble de producto en la línea {linea}")
                                    brazo.bloqueo = True  # El brazo se desocupa
                                    nombreBloqueado = brazo.nombre


                                    posParaEliminar = i
                                    eliminar=True


                                    #self.elaborar.eliminar(i)  # Eliminamos la tarea completada
                                    self.coldDown = self.maquina.tiempo+1  # Iniciamos el tiempo de espera
                            else:  # Si la posición actual es mayor al componente
                                if not brazo.bloqueo: # Si no está bloqueado
                                    brazo.posicionActual -= 1  # Retrocedemos el brazo
                                    print(f"Brazo: {brazo.nombre} retrocediendo a la posición {brazo.posicionActual}")
            cuenta=+1

            if eliminar:
                self.elaborar.eliminar(posParaEliminar)
                eliminar=False
                print("Tarea eliminada")

            # Control de tiempo de espera (coldown)
            if self.coldDown > 0:
                print(f"Enfriamiento: {self.coldDown}")
                self.coldDown -= 1
            else:
                for j in range(self.posicionesBrazos.tamaño):
                    brazo = self.posicionesBrazos.encontrar(j)
                    if brazo.nombre == nombreBloqueado:
                        brazo.bloqueo = False
                        print(f"Brazo {brazo.nombre} desbloqueado")

            print("------------------------------------------------------")
                

            





    



































class matriz:
    def __init__(self, nombre, n, m):
        self.nombre = nombre
        self.n = n  # cantidad de filas
        self.m = m  # cantidad de columnas
        self.filas = listita()  # lista de filas
        relleno = 2023  # Es para rellenar la matriz con algo que sea entero
        contadorn = 0
        while contadorn < n:
            contadorm = 0
            miami = listita() # lista de columnas
            while contadorm < m: 
                miami.agregar(relleno) # Aquí se rellena agrega una celda a la columna
                contadorm += 1 #Hasta que se tiene toda la columna de nodos
            self.filas.agregar(miami) # Aquí se rellena la fila con la columna
            contadorn += 1 # Hasta que termine de tener todas las filas deseadas :)

    def mostrar(self):  # Solo está hecha para ver si lo hice bien (no sirve para nada más)
        contadoro = 0
        while contadoro < self.n: 
            contadori = 0
            print("Fila: ", contadoro + 1)
            while contadori < self.m:
                print(self.filas.encontrar(contadoro).encontrar(contadori))
                contadori += 1
            contadoro += 1

    def encontrar(self, x, y): #Encuentra el dato en la posición indicada
        return self.filas.encontrar(x).encontrar(y) 

    def modificar(self, x, y, dato): #Modifica el dato en la posición indicada
        self.filas.encontrar(x).modificar(y, dato) 

    def encontrarF(self, x): #Encuentra la fila en la posición indicada
        return self.filas.encontrar(x) 
    
    def encontrarC(self, y): #Encuentra la columna en la posición indicada
        return self.columnas.encontrar(y) 

    def sumaModificaEliminaF(self,pos1, pos2): #Suma las filas pos1 y pos2 y lo coloca en la fila pos1
        contador=0

        while contador<self.m: #Recorre toda la fila y va sumando los elementos de las dos filas en las posiciones indicadas
            luis=self.encontrarF(pos1).encontrar(contador)
            fonsi=self.encontrarF(pos2).encontrar(contador)
            luisfonsi=luis+fonsi #guardando la suma de los dos valores
            self.encontrarF(pos1).modificar(contador,luisfonsi) #modificando la fila en la posición indicada---------------------------------------------------------------
            #self.modificar(x,contador,luisfonsi) #Es una opción alternativa que se quedará por cualquier coas :)
            contador+=1
        self.filas.eliminar(pos2) #Eliminando la fila que se sumó
        self.n-=1 #bajando la cantidad de filas



