import pymysql
from flask import Flask, jsonify, request, session
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

MySql = MySQL()
app.config['SECRET_KEY'] = 'the random string'
app.config['MYSQL_DATABASE_USER'] = 'antoine'
app.config['MYSQL_DATABASE_PASSWORD'] = 'azerty'
app.config['MYSQL_DATABASE_DB'] = 'testjb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8880
MySql.init_app(app)

@app.route('/userlist')
def userlist():
    try:
        connection =MySql.connect()
        Pointer = connection.cursor(pymysql.cursors.DictCursor)
        Pointer.execute("SELECT * FROM users WHERE role = 0")
        record = Pointer.fetchall()
        response = jsonify(record)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        Pointer.close()
        connection.close()
@app.route('/company_user/<int:id>')
def company_user(id):
    try:
        connection =MySql.connect()
        Pointer = connection.cursor(pymysql.cursors.DictCursor)
        Pointer.execute("SELECT u.nom, u.prenom, c.nom as nom_entreprise, c.secteur,c.secteur, c.description, c.site_web, c.tel, c.mail FROM users as u, companies as c WHERE u.id = c.idUser and u.id=%s", id)
        record = Pointer.fetchall()
        response = jsonify(record)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        Pointer.close()
        connection.close()

@app.route('/users/<int:id>')
def userbyid(id):
    try:
        connection =MySql.connect()
        Pointer = connection.cursor(pymysql.cursors.DictCursor)
        Pointer.execute("SELECT * FROM users WHERE id=%s", id)
        record = Pointer.fetchone()
        response = jsonify(record)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        Pointer.close()
        connection.close()

@app.route('/register', methods=['POST'])
def add_user():
    try:
        connection = MySql.connect()
        cursor = connection.cursor()
        myform = request.get_json()
        nom = myform['nom']
        prenom = myform['prenom']
        mail = myform['mail']
        mdp = myform['mdp']
        role = myform['role']
        tel = myform['tel']
        hash_mdp = generate_password_hash(mdp)
        SQL_Query = "INSERT INTO `users`(`nom`, `prenom`, `mail`, `mdp`, `role`, `tel`) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(SQL_Query, (nom, prenom, mail, hash_mdp, role, tel))
        connection.commit()
        response = jsonify('Utilisateur ajouté !')
        response.status_code = 200
        return jsonify(response)
    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')
            response.status_code = 400
    finally:
        if role == 1:
            idUser = cursor.lastrowid
            nomEntreprise = myform['nomEntreprise']
            secteur = myform['secteur']
            ville = myform['ville']
            description = myform['description']
            siteweb = myform['site_web']
            telEntreprise = myform['telEntreprise']
            mailEntreprise = myform['mailEntreprise']
            queryEntreprise = "INSERT INTO `companies`(`nom`, `secteur`, `ville`, `description`, `site_web`, `tel`, `mail`, `idUser`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(queryEntreprise, (nomEntreprise, secteur, ville, description, siteweb, telEntreprise, mailEntreprise, idUser))
            connection.commit()
            response = jsonify('Utilisateur ajouté !')
            response.status_code = 200
            return jsonify(response)
        cursor.close()
        connection.close()

@app.route('/login', methods=['POST'])
def login():
    try:
        connection = MySql.connect()
        cursor = connection.cursor()
        myform = request.get_json()
        mail = myform['mail']
        mdp = myform['mdp']
        cursor.execute('SELECT id, mdp, mail  FROM users WHERE mail = % s', (mail))
        account = cursor.fetchone()
        hash_mdp = account[1]
        if check_password_hash(hash_mdp, mdp):
            return jsonify(id = account[0], mail = account[2], connecter = True)
        else:
            return jsonify(msg = 'Incorrect username / password !')
    except Exception as e:
        print(e)
        response = jsonify('Failed to add user.')
        response.status_code = 400
    finally:
        cursor.close()
        connection.close

@app.route('/delete/<int:id>')
def deleteUser(id):
    try:
        connection = MySql.connect()
        Pointer = connection.cursor(pymysql.cursors.DictCursor)
        Pointer.execute("DELETE FROM users WHERE id=%s", id)
        connection.commit()
        msg = "suppression"
    except Exception as e:
        print(e)
        msg = "erreur"
    finally:
        Pointer.close()
        connection.close()
        return jsonify(msg = msg)

@app.route('/addAd', methods=['POST'])
def addAd():
    try:
        connection = MySql.connect()
        cursor = connection.cursor()
        myAd = request.get_json()
        poste = myAd['poste']
        type_emploi = myAd['type_emploi']
        secteur_activite = myAd['secteur_activite']
        ville = myAd['ville']
        salaire = myAd['salaire']
        description = myAd['description']
        entreprise = myAd['entreprise']
        idUserEntreprise = myAd['idUser']
        sql = "INSERT INTO `advertisements`( `poste`, `type_emploi`, `secteur_activite`, `ville`, `salaire`, `description`, `entreprise`, `idUserCompany`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (poste, type_emploi, secteur_activite, ville, salaire, description, entreprise, idUserEntreprise))
        connection.commit()
        response = 'Annonce ajouté !'
    except Exception as e:
        print(e)
        response = 'Erreur'
    finally:
        return jsonify(response)
        cursor.close()
        connection.close

if __name__ == '__main__':
    app.run()
