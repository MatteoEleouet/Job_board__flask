from flask import jsonify
from sqlalchemy.dialects.mysql import pymysql

from app import app, MySql


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