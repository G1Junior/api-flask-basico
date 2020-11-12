#Importa Elementos
from flask import Flask,jsonify, request
#Importa Modulos
from flask_mysqldb import MySQL

#app
app = Flask(__name__)

#Cors (pip install -U flask-cors)
from flask_cors import CORS, cross_origin
cors = CORS(app)

#config DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'apex'
app.config['MYSQL_DB'] = 'aula06'
mysql = MySQL(app)

#Rotas
@app.route('/', methods=['GET'])

def padrao ():
    cursor = mysql.connection.cursor()
    cursor.execute("select * FROM usuarios")
    vetor = cursor.fetchall()
    cursor.close()

    estrutura = []
    conteudo = {}

    for indice in vetor:
        conteudo = ({'codigo': indice[0], 'nome' : indice[1], 'idade': indice[2]})
        estrutura.append(conteudo)
        conteudo = {}
    return jsonify(estrutura)

@app.route('/', methods=['POST'])
def cadastrar():
    try:
        nome = request.form['nome']
        idade = request.form['idade']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuarios (nome, idade) VALUES (%s, %s)", (nome,idade))
        cursor.connection.commit()
        cursor.close()
        return jsonify({"mensagem":"cadastroRealizado"})
    except:
        return jsonify({"mensagem":"Falha ao cadastrar"})

@app.route('/<codigo>', methods=['DELETE'])
def remover(codigo):
    #Validar exclusão
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE codigo = %s", (codigo))
    contagem = cursor.fetchone()[0]
    cursor.close()

    #Condicional
    if contagem == 0:
        return jsonify({"mensagem":"Falha ao remover"})
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM usuarios WHERE codigo = %s", (codigo))
        cursor.connection.commit()
        cursor.close()
        return jsonify({"mensagem":"Usuario deletado!"})




#Servidor
app.run()
