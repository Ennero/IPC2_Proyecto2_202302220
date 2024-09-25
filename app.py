from flask import Flask, render_template, request, redirect, url_for, flash
import procesos as pr


app = Flask(__name__)
app.secret_key = 'my_secret_key'  # Clave secreta que no sé para qué sirve


@app.route('/', methods=['GET','POST']) #Página de inicio
def home(): #Función de la página de inicio
    if request.method == 'POST':
        valor=request.form['id'] #Lee el valor del botón que se presionó
        if(valor=='inicializar'): #Si lee el valor del botón de inicializar
            pr.limpiar() #Inicializa xd
        
        if valor == 'cargar': #Si lee el valor del botón de cargar
            return redirect(url_for('cargar'))
    
    return render_template('page.html') #Mostrar el html de la página


@app.route('/cargar', methods=['GET','POST']) #Página de carga
def cargar():
    if request.method == 'POST':
        ruta=request.form['ruta'] #Lee la ruta del archivo
        pr.cargarXML(ruta) #Carga el archivo

    #Aquí meteré más cosas





        return redirect(url_for('home'))
    
    return render_template('ruta.html')

@app.route('/mensaje', methods=['GET','POST']) #Página de mensajes
def mensaje():
    if request.method == 'POST':
        mensaje=request.form['mensaje'] #Lee el mensaje


if __name__ == '__main__':
    app.run(debug=True)