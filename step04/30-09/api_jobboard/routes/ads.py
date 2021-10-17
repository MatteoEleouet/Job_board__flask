from flask import request, jsonify
from app import app, MySql


@app.route('/api/addAd', methods=['POST'])
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