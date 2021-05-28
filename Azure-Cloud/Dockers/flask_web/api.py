
"""Code for a flask API to Create, Read, Update, Delete users"""
import os
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "adm@bancoentrevista.mysql.database.azure.com"
app.config["MYSQL_ROOT_PASSWORD"] = os.getenv("db_root_password")
app.config["MYSQL_DATABASE_DB"] = ""
app.config["MYSQL_DATABASE_HOST"] = "bancoentrevista.mysql.database.azure.com"

mysql.init_app(app)


@app.route("/")
def index():
    """Function to test the functionality of the API"""
    return "Hello, world!"


@app.route("/version", methods=["GET"])
def version():
    """Function to retrieve all users from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION();")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))

@app.route("/list_databases", methods=["GET"])
def list_databases():
    """Function to retrieve all users from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))

       
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3081)