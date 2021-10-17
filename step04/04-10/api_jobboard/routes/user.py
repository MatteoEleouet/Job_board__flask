import pymysql
from flask import jsonify, request

from app import app, MySql

@app.route('/api/users/get/<int:id>', methods=['GET'])
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

@app.route('/api/users/update/<int:id>', methods=['POST'])
def updateInfoUser(id):
    try:
        myForm = request.get_json()
        nom = myForm['nom']
        prenom = myForm['prenom']
        mail = myForm['mail']
        tel = myForm['tel']
        sql = "UPDATE `users` SET `nom`= %s,`prenom`= %s,`mail`= %s,`tel`= %s WHERE id = %s"
        connection = MySql.connect()
        pointer = connection.cursor()
        data = (nom, prenom, mail, tel, id)
        pointer.execute(sql, data)
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        return jsonify('Informations mises à jour')


@app.route('/api/users/applyjob/<int:idCandidat>/<int:idAd>', methods=['POST'])
def apply(idCandidat, idAd):
    try:
        myForm = request.get_json()
        message = myForm['message']
        sql = "INSERT INTO `job_application`(`idOffreEmploi`, `idUtilisateur`, `message`) VALUES (%s,%s,%s)"
        data = (idAd, idCandidat, message)
        connection = MySql.connect()
        Pointer = connection.cursor()
        Pointer.execute(sql, data)
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        return jsonify('Vous avez postulé à cette offre')
        Pointer.close()
        connection.close()

@app.route('/api/users/allapplies/<int:id>', methods=['GET'])
def listUserApplies(id):
    try:
        connection = MySql.connect()
        Pointer = connection.cursor()
        Pointer.execute("SELECT advertisements.poste, advertisements.type_emploi, advertisements.ville, job_application.date_postule FROM advertisements, job_application WHERE job_application.idUtilisateur = %s and advertisements.id = job_application.idOffreEmploi", id)
        resultat = Pointer.fetchall()
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        return jsonify(resultat)
        Pointer.close()
        connection.close()
