from graphviz import Digraph
import xml.etree.ElementTree as ET
import apuntador as ap

#Defino las listas que voy a utilizar
#La estructura con la que guardaré todo es la siguiente:

#Todas las maquinas en una lista de listas
listaMaquinas=ap.listita()
#Tamaño máximo de la sublista=4 [nombre, cantidadP,cantidadC,tiempo]

#Los productos de cada maquina en una lista de listas
productos=ap.listita()
#Tamaño máximo de la sublista=2 [nombre y elaboracion]





def inicializar():
    pass





def lecturaXML(ruta): #Carga el archivo .xml a las listas con los valores
    global listaMaquinas, productos
    
    try: #El manejo de errores
        arbol=ET.parse(ruta) #Carga el archivo
        ramas=arbol.getroot() #Obtiene la raíz del archivo

        for i in ramas.iter("Maquina"): #Recorre maquinas
            listatemporal1=ap.listita() #Lista temporal para las maquinas
            listatemporal2=ap.listita() #Lista temporal para los productos de cada máquina

        #Primero agrego los valores de las maquinas
            for j in i.iter("NombreMaquina"): #1
                text=j.text
                listatemporal1.agregar(text)
            for j in i.iter("CantidadLineasProduccion"): #2
                text=j.text
                listatemporal1.agregar(text)
            for j in i.iter("CantidadComponentes"): #3
                text=j.text
                listatemporal1.agregar(text)
            for j in i.iter("TiempoEnsamblaje"): #4
                text=j.text
                listatemporal1.agregar(text)
            listaMaquinas.agregar(listatemporal1) #Agrego la lista temporal a la lista de maquinas

        #Luego agrego los valores de los productos de cada máquina
            for j in i.iter("ListadoProductos"):
                for k in j.iter("Producto"):
                    listamuchomastemporal=ap.listita()
                    for l in k.iter("nombre"):
                        text=l.text
                        listamuchomastemporal.agregar(text)
                    for l in k.iter("elaboracion"):
                        text=l.text
                        listamuchomastemporal.agregar(text)
                    listatemporal2.agregar(listamuchomastemporal) #Agrego la lista temporal de cada producto a la lista temporal de productos
                productos.agregar(listatemporal2) #Agrego la lista temporal a la lista de productos
    except Exception as e:
            print(f"Error al cargar el archivo: {e}")

    
    #Comprobando que todo se guardó correctamente :)
    '''j=0
    while j<listaMaquinas.tamaño:
        listaMaquinas.encontrar(j).mostrar()
        j+=1'''
    '''j=0
    while j<productos.tamaño:
        productos.encontrar(j).encontrar(0).mostrar()
        j+=1'''
    '''print(productos.encontrar(0).encontrar(0).encontrar(1))'''
    #-------------------------------------------------------



ruta="C:\prueba1.xml"
lecturaXML(ruta)