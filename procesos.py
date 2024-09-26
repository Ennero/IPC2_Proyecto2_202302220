from graphviz import Digraph
import xml.etree.ElementTree as ET
import apuntador as ap
import copy

#Defino las listas que voy a utilizar
#La estructura con la que guardaré todo es la siguiente:

#Todas las maquinas en una lista de listas
listaMaquinas=ap.listita()


def limpiar(): #Inicializa las listas
    listaMaquinas.vaciar()

def cargarXML(ruta): 
    global listaMaquinas
    
    try:
        arbol = ET.parse(ruta)  # Cargar el archivo XML
        ramas = arbol.getroot() # Obtener la raíz del archivo
        print(ruta)
        
        for i in ramas.iter("Maquina"):  # Recorrer las ramas del archivo
            
            # Variables para guardar los datos de la máquina
            nombre = None
            lineas = None
            listaProductos = None
            tiempo = None
            cantidadC = None
            
            for j in i.iter("NombreMaquina"):
                nombre = j.text
                
                # Verificar si la máquina ya existe y eliminarla (recorriendo en reverso)
                cuento = listaMaquinas.tamaño - 1
                while cuento >= 0:
                    if nombre == listaMaquinas.encontrar(cuento).nombre:
                        listaMaquinas.eliminar(cuento)
                    cuento -= 1

            for j in i.iter("CantidadLineasProduccion"):
                lineas = j.text
            for j in i.iter("CantidadComponentes"):
                cantidadC = j.text
            for j in i.iter("TiempoEnsamblaje"):
                tiempo = j.text

            listaProductos = ap.listita()
            for j in i.iter("ListadoProductos"):
                for k in j.iter("Producto"):
                    n=None
                    p=None
                    for l in k.iter("nombre"):
                        n=l.text
                    for l in k.iter("elaboracion"):
                        p=l.text
                    producto=ap.producto(n,p)
                    listaProductos.agregar(producto)
                    
            nueva_maquina = ap.maquina(nombre, lineas, listaProductos, tiempo, cantidadC)
            listaMaquinas.agregar(nueva_maquina)
    
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")



def simular(): #Función que simula el proceso
    global listaMaquinas, salida
    contadorMaquinas=0




    pass

def star(): #Función que se encarga de hacer el grafo
    ruta="C:\prueba1.xml"
    cargarXML(ruta)
    print(listaMaquinas.tamaño)
    cargarXML(ruta)
    print(listaMaquinas.tamaño)
    #print(listaMaquinas.encontrar(1).listadoProductos.encontrar(1).nombre)

    # Iniciando la simulación
    print(listaMaquinas.encontrar(2).nombre)
    print(listaMaquinas.encontrar(2).listadoProductos.encontrar(0).nombre)
    probando=ap.simulacion(listaMaquinas.encontrar(2),listaMaquinas.encontrar(2).listadoProductos.encontrar(0))
    probando.simular()

star()


