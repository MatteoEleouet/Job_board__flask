import pymysql
from flask import jsonify

from app import app, MySql


@app.route('/api/admin/list', methods=['GET'])
def listForAdmin():
    try:
        connection = MySql.connect()
        Pointer = connection.cursor(pymysql.cursors.DictCursor)
        Pointer.execute("SELECT * FROM users ")
        record = Pointer.fetchall()
    except Exception as e:
        print(e)
    finally:
        for user in record:
            if user['role'] == 1:
                sql = "SELECT c.nom as nom_entreprise, c.secteur, c.site_web FROM companies as c WHERE c.idUser = %s"
                Pointer.execute(sql, user['id'])
                res = Pointer.fetchone()
                user.update(res)
        response = jsonify(record)
        return response
        Pointer.close()
        connection.close()

@app.route('/api/admin/user/delete/<int:id>', methods=['DELETE'])
def deleteUserFromAdmin(id):
    try:
        connection = MySql.connect()
        Pointer = connection.cursor(pymysql.cursors.DictCursor)
        Pointer.execute("SELECT * FROM users WHERE id=%s", id)
        record = Pointer.fetchone()
        response = jsonify(record)
        response.status_code = 200
    except Exception as e:
        print(e)
    finally:
        if record['role'] == 0:
            Pointer.execute("DELETE FROM users WHERE id=%s", id)
            connection.commit()
            msg = "Utilisateur supprimé"
        elif record['role'] == 1:
            Pointer.execute("DELETE FROM companies WHERE idUser=%s", id)
            connection.commit()
            Pointer.execute("DELETE FROM users WHERE id=%s", id)
            connection.commit()
            msg = "Utilisateur et entreprise supprimé"
        return jsonify(msg)
        Pointer.close()
        connection.close()

@app.route('/api/admin/ad/delete/<int:id>', methods=['DELETE'])
def deleteAdFromAdmin(id):
    try:
        connection = MySql.connect()
        Pointer = connection.cursor(pymysql.cursors.DictCursor)
        Pointer.execute("DELETE FROM advertisements WHERE id=%s", id)
        connection.commit()
        msg = "annonce supprimé"
    except Exception as e:
        print(e)
    finally:
        return jsonify(msg)
        Pointer.close()
        connection.close()