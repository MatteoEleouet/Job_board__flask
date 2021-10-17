from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, MySql


@app.route('/api/register', methods=['POST'])
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
        cursor.execute("SELECT mail FROM users WHERE mail = %s", (mail))
        num = cursor.fetchone()
        print(num)
        if num == None:
            SQL_Query = "INSERT INTO `users`(`nom`, `prenom`, `mail`, `mdp`, `role`, `tel`) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(SQL_Query, (nom, prenom, mail, hash_mdp, role, tel))
            connection.commit()
            response = jsonify('Utilisateur ajouté !')
        else:
            print('Email déjà utilisé')
    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')
    finally:
        if role == 1:
            idUser = cursor.lastrowid
            print(idUser)
            nomEntreprise = myform['nomEntreprise']
            secteur = myform['secteur']
            ville = myform['ville']
            description = myform['description']
            siteweb = myform['site_web']
            queryEntreprise = "INSERT INTO `companies`(`nom`, `secteur`, `ville`, `description`, `site_web`, `idUser`) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(queryEntreprise, (nomEntreprise, secteur, ville, description, siteweb, idUser))
            connection.commit()
            response = 'Utilisateur ajouté !'
        cursor.close()
        connection.close()
        return jsonify(response)

@app.route('/api/login', methods=['POST'])
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