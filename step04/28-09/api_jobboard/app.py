import pymysql
from flask import Flask, jsonify, request
from flaskext.mysql import MySQL


app = Flask(__name__)

MySql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'antoine'
app.config['MYSQL_DATABASE_PASSWORD'] = 'azerty'
app.config['MYSQL_DATABASE_DB'] = 'testjb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8880
MySql.init_app(app)

@app.route('/users')
def userlist():
    connection =MySql.connect()
    Pointer = connection.cursor(pymysql.cursors.DictCursor)
    Pointer.execute("SELECT * FROM users")
    record = Pointer.fetchall()
    response = jsonify(record)
    response.status_code = 200
    return response

@app.route('/users/<int:id>')
def userbyid(id):
    connection =MySql.connect()
    Pointer = connection.cursor(pymysql.cursors.DictCursor)
    Pointer.execute("SELECT * FROM users WHERE id=%s", id)
    record = Pointer.fetchone()
    response = jsonify(record)
    response.status_code = 200
    return response


@app.route('/add', methods=['POST'])
def add_user():
        json = request.json
        nom = json['nom']
        prenom = json['prenom']
        email = json['email']
        mdp = json['mdp']
        role = json['role']
        tel = json['tel']
        if nom and prenom and email and mdp and role and tel and request.method == 'POST':
            SQL_Query = "INSERT INTO users(nom, prenom, email, mdp, role, tel) VALUES(%s, %s, %s, %s, %s, %s)"
            data = (nom, prenom, email, mdp, role, tel)
            connection = MySql.connect()
            Pointer = connection.cursor()
            Pointer.execute(SQL_Query, data)
            connection.commit()
            response = jsonify('Utilisateur ajouté !')
            response.status_code = 200
            return response


if __name__ == '__main__':
    app.run()
