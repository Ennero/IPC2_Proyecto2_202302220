import xml.etree.ElementTree as ET
import apuntador as ap

#Defino las listas que voy a utilizar
#La estructura con la que guardaré todo es la siguiente:

#Todas las maquinas en una lista de listas
listaMaquinas=ap.listita()

carga=0 #codito para los mensajes alert
# 0-nada, 1-carga, 2-modificación,
seleccionado=False
maquina=""
producto=""
subido=False
imagenActiva=False
simulado=False
lista=None
tiempot=False

#Alguna info de la simulación actual
tiempoOptimo=0
reporte=""


def limpiar(): #Inicializa las listas
    global listaMaquinas, carga, maquina, producto, seleccionado, subido, imagenActiva, simulado, tiempoOptimo, reporte, lista, tiempot
    listaMaquinas.vaciar()
    carga=0
    maquina=""
    producto=""
    seleccionado=False
    subido=False
    imagenActiva=False
    simulado=False
    tiempoOptimo=0
    reporte=""
    lista=None
    tiempot=False
    


def cargarXML(ruta): 
    global listaMaquinas, carga
    
    try:
        arbol = ET.parse(ruta)  # Cargar el archivo XML
        ramas = arbol.getroot() # Obtener la raíz del archivo
        print(ruta)
        carga=1 #Cambiar el valor de la variable carga a True para el mensaje FLASH
        
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
                        carga=2
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

def simular(maquina,producto): #Función que simula el proceso
    global listaMaquinas, tiempoOptimo, reporte, simulado
    print(maquina,producto) #Imprime la máquina y el producto
    maquinita=encontrarMaquinaPorNombre(maquina) #Encuentra la máquina por nombre
    posMaquina=int(encontrarPosMaquinaPorNombre(maquina)) #Encuentra la posición de la máquina por nombre
    productito=encontrarProductoPorNombre(producto,posMaquina) #Encuentra el producto por nombre

    #Simulación
    simular1=ap.simulacion(maquinita,productito) #Crea la simulación
    simular1.simular() #Simula el proceso
    #simular1.simularPorSegundos(30) #Simula el proceso
    simular1.reportar() #Reporta el proceso
    simular1.graficar() #Grafica la lista de procesos
    tiempoOptimo=simular1.tiempoOptimo #Guarda el tiempo óptimo
    reporte=simular1.reporte #Guarda el reporte #Recorta el reporte para que no se vea la gráfica
    ayuda='<h1 align="center">REPORTE</h1>'
    open("ReporteSimulación.html","w").write(ayuda+reporte) #Guarda el reporte en un archivo html

def simularPorSegundos(maquina,producto,segundo): #Función que simula el proceso por segundos
    global listaMaquinas, tiempoOptimo, reporte, simulado
    print(maquina,producto) #Imprime la máquina y el producto
    maquinita=encontrarMaquinaPorNombre(maquina) #Encuentra la máquina por nombre
    posMaquina=int(encontrarPosMaquinaPorNombre(maquina)) #Encuentra la posición de la máquina por nombre
    productito=encontrarProductoPorNombre(producto,posMaquina) #Encuentra el producto por nombre

    #Simulación
    simular1=ap.simulacion(maquinita,productito) #Crea la simulación
    simular1.simularPorSegundos(segundo) #Simula el proceso
    simular1.reportar() #Reporta el proceso
    simular1.graficar() #Grafica la lista de procesos
    reporte=simular1.reporte #Guarda el reporte
    ayuda='<h1 align="center">REPORTE</h1>'
    open("ReporteSimulación.html","w").write(ayuda+reporte) #Guarda el reporte en un archivo html


def indent(elem, level=0, hor='\t', ver='\n'): # Función para indentar el archivo (solo lo copié y lo pegué xd)
    i = ver + level * hor
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + hor
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1, hor, ver)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
    
def generarSalida(): #Función que genera el archivo de salida
    global listaMaquinas
    ruta="salida.xml"
    raiz=ET.Element("SalidaSimulacion")
    for i in range(listaMaquinas.tamaño):
        maquina=ET.SubElement(raiz,"Maquina")
        nombreMaquina=ET.SubElement(maquina,"Nombre")
        nombreMaquina.text=listaMaquinas.encontrar(i).nombre
        listadoProductos=ET.SubElement(maquina,"ListadoProductos")
        for j in range(listaMaquinas.encontrar(i).listadoProductos.tamaño):
            producto=ET.SubElement(listadoProductos,"Producto")
            nombreProducto=ET.SubElement(producto,"Nombre")
            nombreProducto.text=listaMaquinas.encontrar(i).listadoProductos.encontrar(j).nombre

            #Simulo el producto para encontrar el resto de la información
            simulado=ap.simulacion(listaMaquinas.encontrar(i),listaMaquinas.encontrar(i).listadoProductos.encontrar(j))
            simulado.simular()

            tiempo=ET.SubElement(producto,"TiempoTotal")
            tiempo.text=str(simulado.tiempoOptimo)
            elaboracion=ET.SubElement(producto,"ElaboracionOptima")
            for k in range(simulado.matriz.tamaño):
                segundo=ET.SubElement(elaboracion,"Tiempo", NoSegundo=str(simulado.matriz.encontrar(k).encontrar(0)))
                for l in range(1,simulado.matriz.encontrar(k).tamaño):
                    linea=ET.SubElement(segundo, "LineaEnsamblaje", NoLinea=str(l))
                    linea.text=simulado.matriz.encontrar(k).encontrar(l)
    
    #Aquí escribo el archivo que acabo de generar
    salida=ET.ElementTree(raiz)
    ET.dump(raiz)
    indent(raiz)

    with open(ruta,"wb") as doc:
        salida.write(doc,encoding="utf-8",xml_declaration=True)

def encontrarListaProductosPorMaquina(nombre): #Función que busca la lista de la maquina por nombre
    global listaMaquinas
    for i in range(listaMaquinas.tamaño):
        if listaMaquinas.encontrar(i).nombre==nombre:
            return listaMaquinas.encontrar(i).listadoProductos
        
def encontrarMaquinaPorNombre(nombre): #Función que busca la maquina por nombre (regresa)
    global listaMaquinas
    for i in range(listaMaquinas.tamaño):
        if listaMaquinas.encontrar(i).nombre==nombre:
            return listaMaquinas.encontrar(i)
        
def encontrarProductoPorNombre(nombre,posMaquina): #Función que busca el producto por su nombre 
    global listaMaquinas
    for i in range(listaMaquinas.encontrar(posMaquina).listadoProductos.tamaño):
        if listaMaquinas.encontrar(posMaquina).listadoProductos.encontrar(i).nombre==nombre:
            return listaMaquinas.encontrar(posMaquina).listadoProductos.encontrar(i)
        
def encontrarPosMaquinaPorNombre(nombre): #Función que busca la posición de la máquina por su nombre
    global listaMaquinas
    for i in range(listaMaquinas.tamaño):
        if listaMaquinas.encontrar(i).nombre==nombre:
            return i
    


#cargarXML("ArchivoPrueba.xml")
#Estoy simulando el monitor :)


#simularPorSegundos("M01PC2","Mouse Inalámbrico",30)
#simular("M01PC2","Mouse Inalámbrico")


