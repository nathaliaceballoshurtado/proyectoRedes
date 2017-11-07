from flask import Flask, request
from flask import render_template
import psycopg2
import urllib.parse as urlparse
import os

url = urlparse.urlparse(os.environ['DATABASE_URL'])
database = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

conn = psycopg2.connect(
            database =database,
            user=user,
            password=password,
            host=host,
            port=port
            )





app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consulta', methods = ['GET', 'POST'] )
def consultar ():
    if request.method == 'POST':
        id = request.form['id']
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM descargas Where id = '""" +  id + """'""")
        filas = cursor.fetchall()
        return render_template("resultado.html", filas = filas)
    
    return render_template('busqueda.html')

@app.route('/insertar', methods = ['GET', 'POST'])
def insertar ():
    cursor = conn.cursor()
    if request.method == 'POST':
        url =  request.form['url']
        id = request.form['id']
        cursor.execute("""INSERT INTO descargas (id, url) VALUES ('""" + id +"""' , '""" + url + """')""")
        cursor.execute(""" COMMIT """)
        return render_template('exito.html') 
    return render_template('subir.html')






if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
