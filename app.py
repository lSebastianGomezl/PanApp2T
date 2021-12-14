# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session, url_for,redirect,session
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

usuarios = {}
productos_panaderias = {"Pan-Frances": [], "Pan-Leche": [], "Pan-Queso": [], "Pan-Croazan": [], "Pan-Mantequilla": [], "Pan-Hawaiano": []}

detalles_productos = {
    "Pan-Frances": {
    "nombre_producto": "Pan Frances",
    "imagen": "/static/panfrances.jpg",
    "cantidad": "1",
    "tiempo": "00:05:00",
    "valor": "$ 5.000"
    },
    "Pan-Leche": {
    "nombre_producto": "Pan Leche",
    "imagen": "/static/panleche.jpg",
    "cantidad": "1",
    "tiempo": "00:01:00",
    "valor": "$ 1.000"
    },
    "Pan-Queso": {
    "nombre_producto": "Pan Queso",
    "imagen": "/static/pandequeso.jpg",
    "cantidad": "1",
    "tiempo": "01:23:00",
    "valor": "$ 3.000"
    },
    "Pan-Croazan": {
    "nombre_producto": "Pan Croazan",
    "imagen": "/static/pancroasan.jpg",
    "cantidad": "1",
    "tiempo": "00:50:00",
    "valor": "$ 1.800"
    },
    "Pan-Mantequilla": {
    "nombre_producto": "Pan Mantequilla",
    "imagen": "/static/panmantequilla.jpg",
    "cantidad": "1",
    "tiempo": "00:45:00",
    "valor": "$ 5.000"
    },
    "Pan-Hawaiano": {
    "nombre_producto": "Pan Hawaiano",
    "imagen": "/static/panhawuaino.jpg",
    "cantidad": "1",
    "tiempo": "00:30:00",
    "valor": "$ 3.500"
    }

}

app = Flask(__name__)
app.secret_key = "ajhsdg56dkgasdhbs"

#/ hace referencia a la url base: http://127.0.0.1:5000/
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/panaderias')
def panaderias():
    return render_template('panaderias.html')

@app.route('/formularioregistro')
def interfaz_registrarse():
    return render_template('formularioregistro.html')

@app.route('/formulariologin')
def interfaz_login():
    return render_template('formulariologin.html')


@app.route('/interfazproductos')
def interfaz_productos():
    if 'user' in session:
        return render_template('productos.html', mostrar_login=False)
    return render_template('productos.html', mostrar_login=True)


@app.route('/cerrar')
def cerrar_sesion():
    if 'user' in session:
        session.pop("user")
        return render_template('vuelvepronto.html')
    return render_template('iniciosesionobligatorio.html')

#aca creamos una ruta con un parametro de ruta
#el cual indicara el curso al que inscribir al usuario
@app.route('/comprarproductos/<producto>')
def comprar_productos(producto):
    #aca verificamos si la cookie es valida y extraemos el correo
    #del usuario
    if 'user' in session:
        print("parametro de ruta que llega: ", producto)
        #aca extraemos el email del usuario
        correo = session['user']
        #HACEMOS LA COMPRA DEL PRODUCTO MEDIANTE SU CORREO
        if producto == "Pan-Frances" or producto == "Pan-Leche" or producto == "Pan-Queso" or producto == "Pan-Croazan" or producto == "Pan-Mantequilla" or producto == "Pan-Hawaiano":
            productos_panaderias[producto].append(correo)
        else:
            return render_template('productoexistente.html'), 401
        print("productos comprados", productos_panaderias)
       # nombre = usuarios[correo]["nombre"]
        #return "Señ@r {} usted ha comprado {} ".format(nombre, producto), 201
        return redirect('/productos')
    return render_template('porfavoriniciesesion.html')
        

@app.route('/carrito')
def carrito():
    if 'user' in session:
        correo = session['user']
        #{"pan_frances": [], "pan_de_leche": [], "pan_de_queso": [], 
        # "pan_croazan": [], "pan_mantequilla": [], "pan_hawaiano": []}
        arreglo_productos = []
        for producto in productos_panaderias:
            for correo_usuario in productos_panaderias[producto]:
                if correo_usuario == correo:
                    producto_comprado =[]
                    producto_comprado.append(detalles_productos[producto]["nombre_producto"])
                    producto_comprado.append(detalles_productos[producto]["imagen"])
                    producto_comprado.append(detalles_productos[producto]["cantidad"])
                    producto_comprado.append(detalles_productos[producto]["tiempo"])
                    producto_comprado.append(detalles_productos[producto]["valor"])
                    arreglo_productos.append(producto_comprado)
        return render_template('carrito.html', arreglo_productos=arreglo_productos)
    return render_template('porfavoriniciesesion.html')


@app.route('/quitarproducto/<producto>')
def quitar_producto(producto):
    
    return "Usted ha quitado el producto {}".format(producto)

@app.route('/compra')
def confirmar_compra():
     if 'user' in session:
        correo = session['user']
        proveedor_correo = 'smtp.live.com: 587'
        remitente = 'SGomez0526@outlook.es'
        password = '1094956106Sebas'
        #conexion a servidor
        servidor = smtplib.SMTP(proveedor_correo)
        servidor.starttls()
        servidor.ehlo()
        #autenticacion
        servidor.login(remitente, password)
        #mensaje 
        mensaje = """"<table>
    <tr>
    <th> Gracias por confiar en nosotros </th>
    <th> Su compra fue realizada de manera exitosa </th>
    <th> No olvide pasar por sus productos </th>
  </tr>
  <tr>
    <td>PanApp</td>
    <td>Nit: 457443453</td>
    <td>Ciudad: Armenia-Quindio</td>
    <td>Email: panapp.9490@gmail.com</td>
  </tr>
</table>"""             
        msg = MIMEMultipart()
        msg.attach(MIMEText(mensaje, 'html'))
        msg['From'] = remitente
        msg['To'] = correo
        msg['Subject'] = 'Bienvenido a PanApp Su compra se realizó de forma exitosa'
        servidor.sendmail(msg['From'] , msg['To'], msg.as_string())
        return render_template('confirmarcompra.html')


@app.route('/finalizarcompra', methods=["POST"])
def finalizar_compra():
    return render_template('compraexitosa.html')


@app.route('/registro', methods=['POST'])
def registro():
    correo = request.form.get("correo")
    password = request.form.get("password")
    nombre = request.form.get("nombre")
    apellidos = request.form.get("apellidos")
    direccion = request.form.get("direccion")
    ciudad = request.form.get("ciudad")
    print("--------",correo, password, nombre,apellidos,direccion, ciudad)
    usuarios[correo] = {}
    usuarios[correo]["password"] = password
    usuarios[correo]["ciudad"] = ciudad
    usuarios[correo]["nombre"] = nombre
    usuarios[correo]["apellidos"] = apellidos
    usuarios[correo]["direccion"] = direccion
    usuarios[correo]["ciudad"] = ciudad
    print("diccionario de usuarios: ", usuarios)
    #credenciales
    proveedor_correo = 'smtp.live.com: 587'
    remitente = 'SGomez0526@outlook.es'
    password = '1094956106Sebas'
    #conexion a servidor
    servidor = smtplib.SMTP(proveedor_correo)
    servidor.starttls()
    servidor.ehlo()
    #autenticacion
    servidor.login(remitente, password)
    #mensaje 
    mensaje = """"<table>
  <tr>
    <th> Gracias por confiar en nosotros </th>
    <th> Esperemos satisfacer sus necesidades </th>
  </tr>
  <tr>
    <td>PanApp</td>
    <td>Nit: 457443453</td>
    <td>Ciudad: Armenia-Quindio</td>
    <td>Email: panapp.9490@gmail.com</td>
  </tr>
</table>"""             
    msg = MIMEMultipart()
    msg.attach(MIMEText(mensaje, 'html'))
    msg['From'] = remitente
    msg['To'] = correo
    msg['Subject'] = 'Bienvenido a PanApp Su registro se realizó de forma exitosa'
    servidor.sendmail(msg['From'] , msg['To'], msg.as_string())
    return redirect('/formulariologin')

@app.route('/login', methods=["POST"])
def login():
    correo = request.form.get("correo")
    password = request.form.get("password")
    print("----------",correo,password)
    if usuarios.get(correo):
        if usuarios[correo]["password"] == password:
            nombre=usuarios[correo]["nombre"]
            #generamos cookie de sesion igual al correo de usuario
            #tabien, podriamos hacerlo con el id de base de datos etc
            #tambein, podriamos agregar mas valores a la cookie
            session['user'] = correo
            return render_template("bienvenida.html", nom_usuario = nombre)
        return render_template('datosincorrectos.html')
    return render_template('iniciosesionobligatorio.html'),401
app.run(debug = True, port=5000)