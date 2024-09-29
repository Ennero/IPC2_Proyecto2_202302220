from flask import Flask, render_template, request, redirect, url_for, flash
import procesos as pr


app = Flask(__name__)
app.secret_key = 'my_secret_key'  # Clave secreta que no sé para qué sirve




@app.route('/', methods=['GET','POST'])  # Página de inicio
def home(): #Función de la página de inicio
    if request.method == 'POST':
        valor = request.form.get('id') #Lee el valor del botón que se presionó

        if valor == 'inicializar': #Si lee el valor del botón de inicializar
            pr.limpiar() #Inicializa
            flash('Inicializado con éxito', 'success') #Mensaje de éxito
            return redirect(url_for('home'))
        
        if valor == 'cargar': #Si lee el valor del botón de cargar
            return redirect(url_for('cargar'))

        if valor == 'generar': #Si lee el valor del botón de generar
            pr.generarSalida() #Genera el archivo de salida
            flash('Archivo de salida generado con éxito', 'success') #Mensaje de éxito
            return redirect(url_for('home'))

        #Si no se encontró un valor 'id', verifica si se envió el valor de 'maquina'
        maquina = request.form.get('maquina')

        if maquina: #Verifica si 'maquina' fue enviado en el formulario
            flash(f'Maquina {maquina} seleccionada', 'success') #Mensaje de éxito
            lista = pr.encontrarListaProductosPorMaquina(maquina) #Busca la lista de productos por máquina
            pr.seleccionado = True #Cambia el valor de la variable seleccionado
            pr.maquina = maquina #Guarda el valor de la máquina seleccionada
            return render_template('page.html', lista=pr.listaMaquinas, listaProductos=lista, subido=pr.subido,seleccionado=pr.seleccionado,maquinaN=maquina) #Mostrar el html de la página
        
        producto = request.form.get('producto') #Verifica si 'producto' fue enviado en el formulario
        if producto:
            flash(f'Producto {producto} seleccionado', 'success') #Mensaje de éxito
            pr.simular(pr.maquina,producto) #Simula el proceso


        return redirect(url_for('home'))
    
    # Para GET o si no hay post-data
    return render_template('page.html', lista=pr.listaMaquinas, subido=pr.subido,seleccionado=pr.seleccionado)  # Mostrar el html de la página

@app.route('/tabla') #Página de tabla
def tabla():
    return render_template('mostrartabla.html')

@app.route('/acercade') #Página de acerca de
def acercade():
    return render_template('acercade.html')

@app.route('/estudiante') #Página de información del estudiante
def estudiante():
    return render_template('estudiante.html')


@app.route('/cargar', methods=['GET','POST']) #Página de carga
def cargar():
    global carga
    if request.method == 'POST':
        ruta=request.form['ruta'] #Lee la ruta del archivo
        pr.cargarXML(ruta) #Carga el archivo
        if pr.carga==1:
            flash('Archivo cargado con éxito', 'success')
            pr.subido=True
        else:
            if pr.carga==2:
                flash('Se modificaron maquinas existentes', 'success')
        return redirect(url_for('home'))
    return render_template('ruta.html')



if __name__ == '__main__':
    app.run(debug=True)